#!/usr/bin/env python

import logging
from threading import Thread, Event
import time

import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader, loadUiType
from PySide6.QtCore import Signal, Slot
import pyqtgraph as pg

try:
    # Import from system installed library
    from siglent_sds import SDS_Base
except:
    # If that fails, try loading from parent directory as we might be running
    # in the examples within the source directory, without the library installed.
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from siglent_sds import SDS_Base


class PyQtGraph_Window(*loadUiType(__file__.removesuffix(".py") + ".ui")):

    #  Note: signals need to be defined inside a QObject class/subclass.
    #: :class:`QtCore.Signal` to indicate new data acquisition.
    data_acquired = Signal(list, np.ndarray, np.ndarray)

    def __init__(self):
        """
        Plot live data from the SDS8000X HD in a PyQtGraph window.
        """
        super().__init__(parent=None)
        self.setupUi(self)

        #: PyQtGraph :class:`~pyqtgraph.PlotItem` inside the :class:`~pyqtgraph.GraphicsLayoutWidget`.
        self.plot = self.graphicsLayoutWidget.addPlot()
        self.plot.setLabels(bottom="Time (s)", left="Value")
        self.waves = {
            "C1": self.plot.plot(pen=(255, 255, 0), antialias=False),
            "C2": self.plot.plot(pen=(255, 0, 255), antialias=False),
            "C3": self.plot.plot(pen=(0, 255, 255), antialias=False),
            "C4": self.plot.plot(pen=(0, 192, 0), antialias=False),
            "F1": self.plot.plot(pen=(255, 128, 0), antialias=False),
            "F2": self.plot.plot(pen=(255, 0, 0), antialias=False),
            "F3": self.plot.plot(pen=(0, 0, 255), antialias=False),
            "F4": self.plot.plot(pen=(0, 255, 0), antialias=False),
        }

        # Add numeric input validators to start, stop text boxes
        validator = QtGui.QDoubleValidator()
        validator.setNotation(QtGui.QDoubleValidator.ScientificNotation)
        self.start_lineEdit.setValidator(validator)
        self.size_lineEdit.setValidator(validator)

        # Connect signals
        self.start_pushButton.clicked.connect(self.start_clicked)
        # Connect the signal for new data acquisition
        self.data_acquired.connect(self._update_data)

        #: Thread to run the acquisition in.
        self.thread = None
        #: An :class:`~threading.Event` to indicate the acquisition thread should stop.
        self.stop_acquisition = Event()

    def start_clicked(self):
        """
        Handle starting and stopping of the acquisition when the UI button is clicked.
        """
        if self.start_pushButton.isChecked():
            # Clear existing traces
            for wave in self.waves.values():
                wave.setData()
            # Make and start the background thread to acquire data
            self.thread = Thread(target=self.acquire_data)
            self.stop_acquisition.clear()
            self.thread.start()
            self.configuration_frame.setEnabled(False)
            self.start_pushButton.setText("&Stop")
        else:
            # Stop background thread
            self.stop_acquisition.set()
            self.configuration_frame.setEnabled(True)
            self.start_pushButton.setText("&Start")

    def closeEvent(self, close_event):
        """
        On window close, stop the data acquisition thread and close connection to the device.
        """
        self.stop_acquisition.set()
        if self.thread:
            self.thread.join()

    def _update_data(self, channels, time, data):
        """
        Slot to receive acquired data and update the plot.
        """
        for ch_i, ch in enumerate(channels):
            # Plot first waveform in sequence
            self.waves[ch].setData(time, data[ch_i, 0])
            # Plot mean of waveforms in sequence
            # self.waves[ch].setData(time, np.mean(data[ch_i], axis=0))

    def acquire_data(self):
        """
        Acquire data from the device in a separate thread to the Qt UI.

        The data must be passed back to the Qt thread using the :attr:`data_acquired` signal. It's
        generally OK to read values from the Qt user interface components, but setting values or
        directly updating the pyqtgraph plot will eventually end with bad things happening. The only
        safe way to get data in to the Qt UI is by passing it through a Qt :class:`QtCore.Signal`'s
        :meth:`emit` method.

        In a similar manner, this thread needs to be stopped in a thread-safe manner. This is
        achieved by using the :attr:`stop_acquisition` :class:`~threading.Event` to flag that the
        thread should finish what it's doing and finish execution.
        """

        # Make connection to the device
        sds = SDS_Base(host=self.hostnameLineEdit.text(), waveform_width=(16 if self.hd_checkBox.isChecked() else 8))
        # Wait for connection... crudely
        while not sds.ready():
            if self.stop_acquisition.is_set():
                sds.close()
                return
            time.sleep(0.1)

        # Build channel list from UI checkboxes
        channels = [
            cb.text()
            for cb in self.channels_groupBox.children()
            if type(cb) == QtWidgets.QCheckBox and cb.isChecked()
        ]

        # Configure the device
        sds.channels_enabled(channels)
        sds.sequence(False)
        sds.waveform_interval(self.interval_spinBox.value())
        if self.start_lineEdit.text():
            sds.waveform_start(t=float(self.start_lineEdit.text()))
        else:
            sds.waveform_start()
        if self.size_lineEdit.text():
            sds.waveform_points(t=float(self.size_lineEdit.text()))
        else:
            sds.waveform_points()
        # Start acquisition using single trigger mode
        sds.trigger_mode("single")

        # Loop collecting waveforms and sending back to the Qt UI thread
        while not self.stop_acquisition.is_set():
            # Wait for stop mode indicating single acquisition complete. TODO make a method for TRIG:STAT
            if sds.trigger_status() == "stop":
                ch, t, data = sds.get_waveforms(channels)
                if not data is None:
                    # New waveform data acquired, pass to other thread through the Qt Signal
                    self.data_acquired.emit(ch, t, data)
                    # Restart acquisition
                    sds.trigger_mode("single")
            time.sleep(0.01)

        # Close connection to device
        sds.close()


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=(logging.DEBUG if "--debug" in sys.argv else logging.INFO))

    app = QtWidgets.QApplication(sys.argv)
    window = PyQtGraph_Window()
    window.show()
    sys.exit(app.exec())
