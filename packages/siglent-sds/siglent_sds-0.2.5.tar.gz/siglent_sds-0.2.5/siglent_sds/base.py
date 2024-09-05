import logging
import asyncio
from threading import Thread, Event
import struct
import time
from functools import partial

import numpy as np

from .utils import (
    _wave_descriptor_format,
    _wave_descriptor_format_string,
    timebase_values,
    waveform_sources,
    parse_channel_list,
)
from .connectors import SDS_Socket_Connector


class SDS_Base:
    """
    Base class for a Siglent SDS oscilloscope.

    This class handles the bulk of functionality, but does not implement any actual connection to
    the device. The connection method (e.g. :class:`network
    socket<siglent_sds.connectors.SDS_Socket_Connector>`, USB, USBTMC, VISA) is left up to a
    :class:`~siglent_sds.connectors.SDS_Connector` sub-class. The connector class type (not an
    instance) to use should be passed in as the ``connector`` parameter. By default the
    :class:`~siglent_sds.connectors.SDS_Socket_Connector` will be used that connects via a
    networking socket. All parameters required by the connector (e.g. host ip address) are passed
    through using keyword arguments.

    The parameters that define a particular device model are ``analog_channels``,
    ``waveform_width``, and  ``waveform_grid``. The number of analog channels on the device is
    passed in through the ``analog_channels`` parameter. Standard 8-bit ADC device should use
    ``waveform_width=8`` to specify that acquired data points have 8-bit resolution. For "HD" models
    with 12-bit ADC, use ``waveform_width=16``. The ``waveform_grid`` parameter defines how many
    horizontal grid lines are on the device's display. For all devices this should be 10 except for
    the SHS800X and SHS1000X series which should use ``waveform_grid=12``. The default parameters
    should work for most 4-channel "HD" models.

    Note that there are convenience classes which should set the correct values for the parameters
    for specific devices. See the :mod:`~siglent_sds.devices` submodule for details.

    :param loop: An existing ``asyncio`` event loop to use for scheduling tasks, or None to create a
        new event loop.
    :param connector: A connector class type to use for connecting to the device.
    :param analog_channels: Number of analog channels on the device.
    :param waveform_width: Data point bit width, 8 for normal devices or 16 for HD models.
    :param waveform_grid: Number of grid lines in the horizontal direction, typically 10.
    :param open_device: If ``True`` (default), immediately attempt to open connection to the device.
    :param kwargs: All additional keyword arguments are passed to the connector class.
    """

    def __init__(
        self,
        loop=None,
        connector=SDS_Socket_Connector,
        analog_channels=4,
        waveform_width=16,
        waveform_grid=10,
        open_device=True,
        **kwargs,
    ):
        self._log = logging.getLogger(f"{__name__}.{__class__.__name__}")

        #: Waveform parameters. Structure containing most recent parameters for the waveform source data.
        #: The keys in the dictionary are:
        #:
        #: - ``bandwidth_limit`` - Currently selected channel bandwidth limiter. 0 = off, 1 = 20 MHz, 2 = 200 MHz.
        #: - ``chunk_size_max`` - Maximum number of data points that can be transferred during a single waveform acquisition request.
        #: - ``code_per_div`` - Factor used in conversion of raw waveform ADC data to voltage.
        #: - ``frames_index`` - First frame index to transfer when in sequence mode.
        #: - ``frames_read`` - Number of frames transferred in a single waveform acquisition request when in sequence mode.
        #: - ``frames_sum`` - Total number of frames acquired when in sequence mode.
        #: - ``horizontal_interval`` - Time interval, in seconds, between each data point.
        #: - ``horizontal_offset`` - Horizontal offset in the time axis.
        #: - ``probe_attenuation`` - Attenuation setting selected for the probe, eg 1x or 10x.
        #: - ``time_base`` - Time interval, in seconds, between each horizontal division on the display.
        #: - ``vertical_gain`` - Voltage interval, in volts, between each vertical division on the display.
        #: - ``vertical_offset`` - Vertical offset in the voltage axis.
        #: - ``wave_array_interval`` - Interval between data points in acquired waveforms. For example, if set to 2, every second data point will be returned.
        #: - ``wave_array_max`` - Maximum number of data points possible in a single waveform acquisition. Note that if this is larger than ``chunk_size_max``, multiple waveform requests will be required to collect the entire waveform.
        #: - ``wave_array_points`` - Number of data points to transfer during waveform acquisition requests.
        #: - ``wave_array_start`` - Starting index of data points to transfer during waveform acquisition requests.
        #: - ``wave_source`` - Source channel to use for waveform acquisition requests, for example ``"C1"`` for the first analog channel.
        self.wfp = {
            k: None for k, v in _wave_descriptor_format.items() if not k.startswith("reserved")
        }
        # Add in some extra parameters obtained from queries other than waveform preamble
        self.wfp["chunk_size_max"] = None
        self.wfp["wave_array_points"] = None
        # Sort dictionary keys alphabetically to satisfy OCD
        self.wfp = {k: self.wfp[k] for k in sorted(self.wfp.keys())}

        # Device specific parameters
        #: Number of analog channels on the device.
        self._analog_channels = analog_channels
        #: Data point bit width, 8 ("BYTE") for 8-bit ADC devices, or 16 ("WORD") for 12-bit HD models.
        self._waveform_width = waveform_width
        if type(self._waveform_width) == str:
            if self._waveform_width.upper() == "BYTE":
                self._waveform_width = 8
            else:
                self._waveform_width = 16
        else:
            if not (type(self._waveform_width) == int and self._waveform_width == 8):
                self._waveform_width = 16
        #: Waveform grid numbers in horizontal direction. Default 10 except for SHS800X and SHS1000X is 12.
        self._waveform_grid = waveform_grid

        #: Queue used to buffer commands to be sent to the device.
        self._q = asyncio.Queue()

        #: Event used to create blocking (synchronous) behaviour.
        self._unblock = Event()
        #: Timeout used when blocking on commands, in seconds. Default is 5 seconds.
        self.block_timeout = 5.0
        #: Timeout used when blocking on get_waveforms command, in seconds. Default is 60 seconds.
        self.get_waveforms_timeout = 60.0

        #: Numpy data type to use for acquired waveform time axis. The default is
        #: :attr:`numpy.float32`, but can be changed to :attr:`numpy.float64` or
        #: :attr:`numpy.float16` to trade off precision versus performance and memory use.
        #: Note that the time and data precision are independent, as it my be desirable to keep a
        #: high-precision time axis, but reduced precision data.
        self.waveform_time_dtype = np.float32
        #: Numpy data type to use for acquire waveform data. The default is :attr:`numpy.float32`,
        #: but can be changed to :attr:`numpy.float64` or :attr:`numpy.float16` to trade off
        #: precision versus performance and memory use.
        self.waveform_data_dtype = np.float32

        # Use provided event loop to schedule events, Note this may not have been started yet!
        # If loop is not provided, we will make our own when the device is opened.
        self._loop = loop
        self._thread = None

        # Create the connector class instance to handle the communications with the device
        self._connector = connector(parent=self, **kwargs)
        # Task used to establish and maintain communication channels.
        self._connection_task = None

        if open_device:
            self.open()

    def _run_eventloop(self):
        """
        Entry point for the event loop thread.
        """
        self._log.debug("Starting event loop.")
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()
            self._loop = None
        self._log.debug("Event loop stopped.")

    async def _handle_comms(self):
        """
        Handle communications with the device. We should have valid reader and writer streams
        configured at this point. This coroutine should be called by a connector class once a
        connection has been established.
        """
        self._log.info(f"Connection established with {self._connector.connection_name}.")
        # Keep track of any read errors, may need to flush buffers etc
        last_error = None
        while True:
            try:
                # Get a command from the send queue
                # self._log.debug(f"Waiting for command from queue, current size {self._q.qsize()}.")
                command, delimiter, binary, wait, callback, error_callback = await self._q.get()
                # Check for our special wait instruction to pause communications with device for a while
                if command[0:4] == b"WAIT":
                    # Interpret parameter as wait time in seconds
                    try:
                        wait_time = float(command[4:])
                    except (TypeError, ValueError) as ex:
                        self._log.warning(
                            "Couldn't interpret requested wait time, will use default."
                        )
                        # Default to 1 ms
                        wait_time = 1e-3
                    else:
                        if wait_time <= 0:
                            wait_time = 1e-3
                    self._log.debug(f"Waiting for {wait_time} s before sending next command.")
                    await asyncio.sleep(wait_time)
                    # Ensure we don't try to read a response from the device
                    delimiter = None
                    binary = False
                else:
                    # Normal command to send to device.
                    # First, flush read buffer if errors have occurred previously
                    if last_error:
                        self._log.debug("Previous command failed, first flushing read buffer.")
                        while True:
                            try:
                                async with asyncio.timeout(0.1):
                                    await self._connector.reader.read(1)
                            except asyncio.TimeoutError:
                                break
                        last_error = None
                    # Send command to the device
                    self._log.debug(f"Sending command: {command}")
                    self._connector.writer.write(command)
                    self._connector.writer.write(b"\n")
                    await self._connector.writer.drain()
            except Exception as ex:
                # Something bad happened when trying to send the message
                self._log.error(f"Error writing command: {ex}")
                last_error = ex
            else:
                # Message sent OK, attempt to read a response if one is expected
                # Default is no response
                data_bytes = b""
                if delimiter or binary:
                    # Message expects some sort of response
                    try:
                        if not binary and delimiter:
                            # Text response expected, read until given delimiter is found
                            # self._log.debug(
                            #     f"Waiting for data block from {self._connector.connection_name} delimited by {delimiter}."
                            # )
                            async with asyncio.timeout(2.0):
                                data_bytes = await self._connector.reader.readuntil(
                                    separator=delimiter
                                )
                        elif binary:
                            # Response is binary, header will contain the length of the data
                            # self._log.debug("Waiting for header of fixed-length data block.")
                            # Documentation says first two bytes will be #N, where N is the number of digits to follow
                            # In reality, if no waveform then response looks like "C1:WF DAT2,#9000000000\n\n"
                            # So we'll instead search for the # sign
                            async with asyncio.timeout(1.0):
                                data_header = await self._connector.reader.readuntil(b"#")
                            # if len(data_header) > 1:
                            #     self._log.debug(
                            #         f"Found {len(data_header) - 1} extra bytes before data block header: {data_header[:-1]}"
                            #     )
                            # Now the next byte should be number of digits in the length
                            async with asyncio.timeout(1.0):
                                data_header = await self._connector.reader.readexactly(1)
                            try:
                                header_length = int(data_header[0:1])
                            except (ValueError, IndexError) as ex:
                                self._log.error("Unable to determine length of data block.")
                                last_error = ex
                            else:
                                # self._log.debug(
                                #     f"Waiting for {header_length} bytes containing data block length."
                                # )
                                async with asyncio.timeout(1.0):
                                    data_header = await self._connector.reader.readexactly(
                                        header_length
                                    )
                                try:
                                    block_length = int(data_header)
                                except (ValueError, IndexError) as ex:
                                    self._log.error(
                                        f"Invalid length of data block, received {data_header}."
                                    )
                                    last_error = ex
                                else:
                                    # self._log.debug(
                                    #     f"Header reports {data_header} == {block_length} byte data block to follow."
                                    # )
                                    # Block may also be terminated by a delimiter such as '\n' or '\n\n'
                                    async with asyncio.timeout(1.0):
                                        data_bytes = await self._connector.reader.readexactly(
                                            block_length + len(delimiter)
                                        )
                    except asyncio.TimeoutError as ex:
                        self._log.error("Timeout when reading response.")
                        last_error = ex
                    except asyncio.LimitOverrunError as ex:
                        # Stream limit exceeded, message may be incomplete
                        self._log.error(
                            f"Data block from {self._connector.connection_name} exceeded buffer size."
                        )
                        data_bytes = await self._connector.reader.read(self._buffer_size)
                        # TODO: handle this better, could buffer and continue reading
                        last_error = ex
                    except asyncio.IncompleteReadError as ex:
                        # Connection closed before message completed
                        data_bytes = ex.partial
                        self._log.info(
                            f"Connection with {self._connector.connection_name} closed, but read {len(data_bytes)} bytes."
                        )
                        last_error = ex
                    except (ConnectionResetError, BrokenPipeError, OSError) as ex:
                        self._log.info(f"Connection with {self._connector.connection_name} closed.")
                        last_error = ex
                    else:
                        last_error = None

                    # self._log.debug(f"Received {len(data_bytes)} bytes from {self._connector.connection_name}.")

            # If a wait time specified, wait for some period before continuing
            if wait:
                await asyncio.sleep(wait)

            if last_error and error_callback:
                # Notify of error if any occurred
                error_callback(last_error)
            elif callback:
                # Handle (possibly empty) data by passing to callback function
                callback(data_bytes)

            # Tell the queue we have finished dealing with the item we retrieved
            self._q.task_done()

            # Stop reading if end of file (connection closed)
            if self._connector.reader.at_eof():
                break

    def open(self):
        """
        Open connection to the device and begin processing commands.
        """
        # If an event loop wasn't provided, create our own event loop and thread to run it in.
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
            self._thread = Thread(target=self._run_eventloop, daemon=True)
            self._thread.start()
        # Start the connection task if not already started
        if self._connection_task is None or self._connection_task.done():
            self._connection_task = self._loop.create_task(
                self._connector.open_connection(), name=f"{__class__.__name__} Connector"
            )
        # Queue some configuration and update device parameters
        self.waveform_width(self._waveform_width, block=False)
        self.update_waveform_maxpoints(block=False)
        self.update_waveform_points(block=False)

    def close(self):
        """
        Stop processing commands and close the connection to the device.
        """
        # Cancel the connection task if running
        if not self._loop is None:
            self._log.info("Closing connection.")
            self._loop.call_soon_threadsafe(self._connection_task.cancel)
            # Wait for connection task to finish
            while not self._connection_task.done():
                time.sleep(0.01)
            # Report any exceptions raised within the connection task
            try:
                task_exception = self._connection_task.exception()
                if task_exception:
                    self._log.error("Error in connection task:", exc_info=task_exception)
            except asyncio.CancelledError:
                pass

        # Close connection
        self._connector.close()

        # Stop our event loop thread if we had created one
        if not self._thread is None:
            self._log.debug("Stopping event loop.")
            self._loop.call_soon_threadsafe(self._loop.stop)
            # Wait for thread to finish
            self._thread.join()
            self._thread = None

        # Reset the command queue
        # if not self._q.empty():
        #    self._log.debug("Some commands were queued but weren't processed.")
        self._q = asyncio.Queue()

    def send(
        self,
        command,
        delimiter=b"\n",
        binary=False,
        block=False,
        wait=0.0,
        callback=None,
        error_callback=None,
        timeout=None,
    ):
        """
        Send a SCPI command to the device.

        In most cases responses are delimited by a newline ``b"\\n"``. Some commands do not produce
        a response, in which case ``delimiter=None`` or ``delimiter=b""`` should be used.

        For commands that respond with binary data prefixed with a header indicating the length of
        the response, such as ``"#9123456789"``, use ``binary=True``.

        Synchronous behaviour (blocking) can be enabled by setting the parameter ``block=True``. In
        this case the function will not return until the command has been processed by the device.
        Once the command has completed, any result will be returned as raw :class:`bytes` with any
        delimiter still appended. If no reply is received from the device, empty bytes (``b""``)
        will be returned. If an error occurs during communications or processing of the response,
        the exception will be raised. If the function takes too long to complete, a
        :class:`TimeoutError` will be raised. The ``timeout`` parameter may be given to provide a
        custom timeout delay. If not provided, the default set by :attr:`block_timeout` will be
        used.

        Some commands require some period of time before sending the next command. If that is the
        case, then the ``wait`` parameter specified the delay time, in seconds, before the next
        command will be sent. Note that the callback (or function return if ``block=True``) will not
        occur until after the command is completed and any waiting period has elapsed. If more
        flexibility is required, wait times can be arranged explicitly using the :meth:`wait`
        method.

        Once the command has been processed the optional callback function will be called with the
        returned data. The callback method signature should be ``callback(data)`` where ``data``
        will be a :class:`bytes` object with any delimiter still appended.

        If the optional ``error_callback`` parameter is given, it should be a function of the form
        ``callback(ex)``, where ``ex`` will be an :class:`Exception` which describes the error. If
        an error occurs, the normal callback will not be called.

        Note that callbacks will still be made if synchronous behaviour is requested using the
        ``block=True`` parameter, and they will occur prior to this function returning.

        :param command: The SCPI command to send.
        :param delimiter: Delimiter expected at the end of the response, or ``None``.
        :param binary: Flag to indicate a binary data block response.
        :param block: Block return of function until command completes.
        :param callback: Function to call with response data.
        :param error_callback: Function to call if an error occurs.
        :param timeout: Time to wait for command to complete.
        :returns: Response from the device if ``block=True``.
        """
        # Sanity checks
        if self._loop is None:
            self._log.warning("No event loop active, can't queue commands.")
            return
        if command is None:
            self._log.warning("No command provided, can't send to device.")
            return
        if not ((callback is None) or (callable(callback))):
            self._log.warning("Invalid response callback function, can't send to device.")
            return
        if not ((error_callback is None) or (callable(error_callback))):
            self._log.warning("Invalid error callback function, can't send to device.")
            return

        # Encode strings as bytes using ascii encoding
        if type(command) == str:
            try:
                command = bytes(command, "ascii")
            except:
                self._log.warning("Failed to encode command string as ascii bytes.")
        if type(delimiter) == str:
            try:
                delimiter = bytes(delimiter, "ascii")
            except:
                self._log.warning("Failed to encode delimiter string as ascii bytes.")

        if not type(command) == bytes:
            self._log.warning("Unable to convert command to bytes, can't send to device.")
            return
        if delimiter is None:
            delimiter = b""
        if not type(delimiter) == bytes:
            self._log.warning("Invalid response delimiter, can't send to device.")
            return

        # Ensure wait time looks like a real number
        try:
            wait = float(wait)
        except (TypeError, ValueError) as ex:
            self._log.warning("Couldn't interpret requested wait time, will use 1 ms.")
            wait = 1e-3
        if wait < 0.0:
            wait = 0.0

        # self._log.debug(f"Enqueuing command: {command}")
        if not block:
            # Enqueue command to be sent to the device, return immediately
            self._loop.call_soon_threadsafe(
                self._q.put_nowait, (command, delimiter, bool(binary), wait, callback, error_callback)
            )
        else:
            # Wait for command to complete, then notify callbacks and return result
            global command_result
            global command_exception

            def handle_send(data):
                """
                Handle response from send. Call callback and unblock.
                """
                global command_result
                if callback:
                    callback(data)
                self._unblock.set()
                command_result = data

            def handle_send_error(ex):
                """
                Handle error from send. Call error callback and unblock.
                """
                global command_exception
                if error_callback:
                    error_callback(ex)
                self._unblock.set()
                command_exception = ex

            # Enqueue command to be sent to the device using our callback wrappers and block
            self._loop.call_soon_threadsafe(
                self._q.put_nowait,
                (command, delimiter, bool(binary), wait, handle_send, handle_send_error),
            )
            self._unblock.clear()
            command_result = None
            command_exception = None
            # Wait for command to complete, consider additional delay if a wait time was specified
            if not self._unblock.wait(wait + self.block_timeout if timeout is None else timeout):
                raise TimeoutError(f"Timeout waiting for {command} to complete.")
            if command_exception:
                # Tidy up the timeout exception output a little bit
                if type(command_exception) == TimeoutError:
                    command_exception = TimeoutError(
                        f"Communications timeout during {command} command."
                    )
                raise command_exception
            return command_result

    def ready(self):
        """
        Returns ``True`` if a connection has been made and no commands are currently queued or being
        processed by the system.

        This can be checked so that an excessive number of commands aren't sent to the device faster
        than it can process them.
        """
        return (
            self._q.empty()
            and (not self._connector.reader is None)
            and (not self._connector.writer is None)
        )

    def print_query(self, command_string, delimiter=b"\n", **kwargs):
        """
        A wrapper around :meth:`send` that by default prints the response to stdout.

        The remaining keyword arguments are passed to the :external+python:py:func:`print` method.
        """

        def handle_query(data):
            try:
                print(data.rstrip(b"\n").decode("ascii"), **kwargs)
            except UnicodeDecodeError:
                print(data, **kwargs)

        self.send(command_string, delimiter=delimiter, callback=handle_query)

    def command(self, command_string, block=True, **kwargs):
        """
        A wrapper around :meth:`send` that does not expect a response from the device.

        The ``command_string`` parameter should be a SCPI command string, e.g. ``":WAV:POIN 3000"``.

        Note that this method is synchronous by default and will block until completed.

        :param command_string: SCPI command string to send to the device.
        :param block: Block function return until query completed.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        """
        self.send(command_string, delimiter=b"", block=block, **kwargs)

    def query(self, query_string, block=True, **kwargs):
        """
        A wrapper around :meth:`send` that expects a response delimited by a newline.

        The ``query_string`` parameter should be a SCPI query string, e.g. ``":WAV:MAXP?"``.

        Note that this method is synchronous by default and will block until completed.

        The response will be attempted to be interpreted as an :class:`int`, :class:`float`, or a
        :class:`str`, in that order. If the response cannot be interpreted, raw :class:`bytes` will
        be returned.

        :param query_string: SCPI query string to send to the device.
        :param block: Block function return until query completed.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        :returns: Response from the device from the query.
        """
        response = self.send(query_string, delimiter=b"\n", block=block, **kwargs)
        # Return None if no response
        if not response:
            return None
        # Attempt cast to int
        if type(response) == bytes:
            try:
                response = int(response)
            except ValueError:
                pass
        # Attempt cast to float
        if type(response) == bytes:
            try:
                response = float(response)
            except ValueError:
                pass
        # Attempt cast to str
        if type(response) == bytes:
            try:
                response = response.rstrip(b"\n").decode("ascii")
            except UnicodeDecodeError:
                pass
        # Fall back to raw bytes object if cast attempts fail
        return response

    def wait(self, delay_time=1e-3, **kwargs):
        """
        Wait for a period of time before sending the next command to the device.

        This can be used in the situation where the device misbehaves if a command is sent
        immediately after another. For example, on the Siglent SDS800X HD the ``:TIMebase:SCALe``
        command will likely not work correctly without approximately 1 ms delay before the next
        command is sent.

        :param delay_time: Time to wait before sending next command, in seconds.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        """
        if not "timeout" in kwargs:
            kwargs["timeout"] = delay_time + self.block_timeout
        self.send(f"WAIT {delay_time}", **kwargs)

    def reset(self, block=True, **kwargs):
        """
        Reset the device to defaults settings.

        :param block: Block function return until command completed.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        """
        self.send("*RST", delimiter=b"", block=block, wait=6.0, **kwargs)

    def run(self, block=True, **kwargs):
        """
        Send the run command to the device.

        Note that this method is synchronous by default and will block until completed.

        :param block: Block function return until command completed.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        """
        self.send(":TRIG:RUN", delimiter=b"", block=block, **kwargs)

    def stop(self, block=True, **kwargs):
        """
        Send the stop command to the device.

        Note that this method is synchronous by default and will block until completed.

        :param block: Block function return until command completed.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        """
        self.send(":TRIG:STOP", delimiter=b"", block=block, **kwargs)

    def trigger_mode(self, mode="auto", block=True, **kwargs):
        """
        Configure the trigger mode.

        Options for the ``mode`` parameter are ``"single"``, ``"normal"``, ``"auto"``, or
        ``"force"``.

        Note that this method is synchronous by default and will block until completed.

        :param mode: Trigger mode to select.
        :param block: Block function return until command completed.
        :param kwargs: Remaining keyword arguments are passed to :meth:`send`.
        """
        if mode == "force":
            mode = "FTRIG"
        try:
            self.send(f":TRIG:MODE {mode.upper()}", delimiter=b"", block=block, **kwargs)
        except:
            self._log.exception("Unable to set trigger mode.")

    def trigger_edge(
        self, source=None, level=None, slope=None, block=True, callback=None, error_callback=None
    ):
        """
        Configure edge triggering, and optionally set parameters.

        The ``source`` parameter sets the trigger source channel, which may be any of the analog
        (e.g. ``"C1"``, ``"C2"``) or digital (e.g. ``"D1"``, ``"D2"``) channels, external
        (``"EXT"``), or AC line (``"LINE"``) inputs if they are available on the device. An analog
        channel may also be specified using a single integer.

        The ``level`` parameter sets the threshold signal level, in volts.

        The ``slope`` parameter specifies either rising, falling, or alternating slopes as
        ``slope="rising"``, ``slope="falling"``, or ``slope="alternate"``, respectively.

        :param source: Source channel to use for edge triggering.
        :param level: Signal threshold level for edge triggering.
        :param slope: Slope type for edge triggering.
        :param block: Block function return until command completed.
        :param callback: Function to call once waveform parameter data is ready.
        :param error_callback: Function to call if an error occurs.
        """
        if not source is None:
            if type(source) == int:
                source = f"C{source}"
            self.send(f"TRIG:EDGE:SOUR {source}", delimiter=b"", block=False)
        if not level is None:
            self.send(f"TRIG:EDGE:LEV {level}", delimiter=b"", block=False, wait=0.001)
        if not slope is None:
            self.send(f"TRIG:EDGE:SLOP {slope}", delimiter=b"", block=False)
        self.send(
            "TRIG:TYPE EDGE",
            delimiter=b"",
            block=block,
            callback=callback,
            error_callback=error_callback,
        )

    def trigger_status(self, block=True, **kwargs):
        """
        Query the current state of the trigger.

        The state will be returned as a lowercase string, and should be one of ``"arm"``,
        ``"ready"``, ``"auto"``, ``"trig'd"``, ``"stop"``, or ``"roll"``.

        :param block: Block function return until command completed.
        :param kwargs: Remaining parameters are passed to :meth`send`.
        """
        response = self.send("TRIG:STAT?", delimiter=b"\n", block=block, **kwargs)
        try:
            response = response.rstrip(b"\n").decode("ascii").lower()
        except (AttributeError, UnicodeDecodeError):
            return
        return response

    def acquire_memdepth(self, depth, block=True, callback=None, error_callback=None):
        """
        Configure the maximum memory depth for waveform acquisition.

        The valid values for the ``depth`` parameter vary by device model and the number of active
        channels. The value is specified as as string such as ``"10k"`` or ``"1M"``.

        :param depth: Maximum memory depth for waveform acquisition.
        :param block: Block function return until command completed.
        :param callback: Function to call once waveform parameter data is ready.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f"ACQ:MDEP {depth}",
            delimiter=b"",
            wait=0.1,
            block=block,
            callback=callback,
            error_callback=error_callback,
        )

    def update_waveform_preamble(self, block=True, callback=None, error_callback=None):
        """
        Request the waveform preamble which contains parameters for the current waveform
        acquisition. This will update the parameters stored in the :data:`wfp` dictionary.

        Note that this method is synchronous by default and will block until completed and the
        :data:`wfp` dictionary is updated. Note that if asynchronous behaviour is requested using
        the ``block=False`` parameter then the values in :data:`wfp` will not have been updated yet
        during subsequent code execution.

        The optional ``callback`` parameters should be a function to call once the updated waveform
        parameters are available. The function should be of the form ``callback(waveform_params)``,
        where ``waveform_params`` will be the waveform parameter dictionary :data:`wfp`. The
        ``error_callback`` parameter behaves the same as the :meth:`send` method.

        If the default blocking behaviour is used, then this method will return the :data:`wfp`
        dictionary containing the latest waveform parameters.

        :param block: Block function return until command completed.
        :param callback: Function to call once waveform parameter data is ready.
        :param error_callback: Function to call if an error occurs.
        :returns: Updated :data:`wfp` dictionary if default ``block=True`` parameter used.
        """

        def handle_waveform_preamble(data):
            try:
                # Preamble has newline appended. But also when in sequence mode there seem to be
                # extra bytes which aren't documented in (firmware version 1.1.3.8, documentation
                # revision EN11F). From the example code these seems like timestamps.
                params = struct.unpack(_wave_descriptor_format_string, data[0:346])
            except struct.error:
                self._log.error(f"Unable to interpret :WAV:PRE? response: {data[:-1]}")
                return
            # Dictionary comprehension magic to fill in values to data structure
            self.wfp.update(
                {
                    k: params[i]
                    for i, (k, v) in enumerate(_wave_descriptor_format.items())
                    if not k.startswith("reserved")
                }
            )
            # Convert bytes to strings
            for k, v in self.wfp.items():
                if type(v) == bytes:
                    self.wfp[k] = v.rstrip(b"\x00").decode("ascii")
            # Convert timebase index to actual value from lookup table
            self.wfp["time_base"] = timebase_values[self.wfp["time_base"]]
            # Convert source channel index to actual value from lookup table
            self.wfp["wave_source"] = waveform_sources[self.wfp["wave_source"]]
            # Return updated parameters to callback function if requested
            if callable(callback):
                callback(self.wfp)

        # Waveform preamble contains header with binary data length
        self.send(
            ":WAV:PRE?",
            binary=True,
            block=block,
            callback=handle_waveform_preamble,
            error_callback=error_callback,
        )
        if block:
            return self.wfp

    def update_waveform_maxpoints(self, block=True, callback=None, error_callback=None):
        """
        Request the maximum number of points in an acquisition. This will update the
        ``"chunk_size_max"`` field in the :data:`wfp` dictionary.

        Note that this method is synchronous by default and will block until completed and the
        :data:`wfp` dictionary is updated. Note that if asynchronous behaviour is requested using
        the ``block=False`` parameter then the values in :data:`wfp` will not have been updated yet
        during subsequent code execution.

        The optional ``callback`` parameters should be a function to call once the updated value is
        available. The function should be of the form ``callback(chunk_size_max)``, where
        ``chunk_size_max`` will be the ``chunk_size_max`` parameter from the :data:`wfp` dictionary.
        The ``error_callback`` parameter behaves the same as the :meth:`send` method.

        If the default blocking behaviour is used, then this method will return the updated value.

        :param block: Block function return until command completed.
        :param callback: Function to call once waveform parameter data is ready.
        :param error_callback: Function to call if an error occurs.
        :returns: Maximum number of points in an acquisition if the default ``block=True`` is used.
        """

        def handle_waveform_maxpoints(data):
            try:
                self.wfp["chunk_size_max"] = int(data)
            except ValueError:
                self._log.warning("Unable to determine waveform max points.")
                return
            # Return updated parameters to callback function if requested
            if callable(callback):
                callback(self.wfp["chunk_size_max"])

        self.send(
            ":WAV:MAXP?",
            block=block,
            callback=handle_waveform_maxpoints,
            error_callback=error_callback,
        )
        if block:
            return self.wfp["chunk_size_max"]

    def update_waveform_points(self, block=True, callback=None, error_callback=None):
        """
        Request the number of points returned in an acquisition. This will update the
        ``"wave_array_points"`` field in the :data:`wfp` dictionary.

        The number of points in the waveform can exceed the maximum number of points allowed in a
        single waveform acquisition chunk, meaning the waveform would need to be acquired in several
        chunks.

        Note that this method is synchronous by default and will block until completed and the
        :data:`wfp` dictionary is updated. Note that if asynchronous behaviour is requested using
        the ``block=False`` parameter then the values in :data:`wfp` will not have been updated yet
        during subsequent code execution.

        The optional ``callback`` parameters should be a function to call once the updated value is
        available. The function should be of the form ``callback(wave_array_points)``, where
        ``wave_array_points`` will be the ``wave_array_points`` parameter from the :data:`wfp`
        dictionary. The ``error_callback`` parameter behaves the same as the :meth:`send` method.

        If the default blocking behaviour is used, then this method will return the updated value.

        :param block: Block function return until command completed.
        :param callback: Function to call once waveform parameter data is ready.
        :param error_callback: Function to call if an error occurs.
        :returns: Number of points in an acquisition if the default ``block=True`` is used.
        """

        def handle_waveform_points(data):
            try:
                points = int(data)
                if points == 0:
                    points = self.wfp["wave_array_max"]
                self.wfp["wave_array_points"] = points
            except ValueError:
                self._log.warning("Unable to determine waveform points.")
                return
            # Return updated parameters to callback function if requested
            if callable(callback):
                callback(self.wfp["wave_array_points"])

        self.send(":WAV:POIN?", callback=handle_waveform_points)
        if block:
            return self.wfp["wave_array_points"]

    def update_waveform_parameters(self, block=True, callback=None, error_callback=None):
        """
        Update all entries in the waveform parameters dictionary, :data:`wfp`.

        Note that this method is synchronous by default and will block until completed and the
        :data:`wfp` dictionary is updated. Note that if asynchronous behaviour is requested using
        the ``block=False`` parameter then the values in :data:`wfp` will not have been updated yet
        during subsequent code execution.

        The optional ``callback`` parameters should be a function to call once the updated values
        are available. The function should be of the form ``callback(waveform_params)``, where
        ``waveform_params`` will be the :data:`wfp` dictionary. The ``error_callback`` parameter
        behaves the same as the :meth:`send` method.

        If the default blocking behaviour is used, then this method will return the :data:`wfp`
        dictionary containing the latest waveform parameters.

        :param block: Block function return until command completed.
        :param callback: Function to call once waveform parameter data is ready.
        :param error_callback: Function to call if an error occurs.
        :returns: The updated :data:`wfp` dictionary if the default ``block=True`` is used.
        """

        self.update_waveform_preamble(block=False, error_callback=error_callback)
        self.update_waveform_points(block=False, error_callback=error_callback)
        self.update_waveform_maxpoints(
            block=block, callback=callback, error_callback=error_callback
        )
        if block:
            return self.wfp

    def waveform_data(self, block=True, callback=None, error_callback=None):
        """
        Request the current waveform data.

        The callback function should be of the form ``callback(t, y)``, where ``t`` is the time axis
        labels in seconds, and ``y`` is the channel data in volts.

        Does not handle the case that waveform retrieval needs to be done in several chunks, so
        limited to 5 M data points. See the :meth:`get_waveforms` method for a higher-level routine
        to retrieve large waveforms from multiple channels.

        If the default ``block=True`` is used, the time axis and waveform data will be returned from
        this method.

        :param block: Block function return until command completed.
        :param callback: Callback function to provide the waveform data to.
        :param error_callback: Function to call if an error occurs.
        :returns: Time axis and waveform data if ``block=True`` is used.
        """

        def handle_waveform_data(data):
            # Empty data will still contain the two \n termination characters
            if len(data) <= 2:
                self._log.debug("No data was received from waveform request.")
                return
            data = np.frombuffer(
                data[:-2], dtype=(np.int16 if self._waveform_width == 16 else np.int8)
            )
            data = (
                data * (self.wfp["vertical_gain"] / self.wfp["code_per_div"])
                - self.wfp["vertical_offset"]
            )
            time = (
                self.wfp["horizontal_offset"]
                - (self.wfp["time_base"] * self._waveform_grid / 2)
                + np.arange(
                    start=self.wfp["wave_array_start"],
                    stop=self.wfp["wave_array_start"]
                    + (self.wfp["wave_array_points"] * self.wfp["wave_array_interval"]),
                    step=self.wfp["wave_array_interval"],
                    dtype=self.waveform_time_dtype,
                )
                * self.wfp["horizontal_interval"]
            )
            if not callable(callback):
                self._log.debug(
                    f"Waveform data received. Length {len(data)} points, t = {time[0]:g} to {time[-1]:g}. Data min|mean|max = {data.min():g}|{data.mean():g}|{data.max():g}."
                )
                self._log.debug(
                    f"chunk_size_max={self.wfp['chunk_size_max']}, wave_array_points={self.wfp['wave_array_points']}, wave_array_start={self.wfp['wave_array_start']}, wave_array_interval={self.wfp['wave_array_interval']}"
                )
                self._log.debug(
                    f"frames_read={self.wfp['frames_read']}, frames_sum={self.wfp['frames_sum']}, frames_index={self.wfp['frames_index']}"
                )
            else:
                callback(time, data)

        self.update_waveform_parameters(block=False, error_callback=error_callback)
        # Waveform data contains header with binary data length
        data = self.send(
            ":WAV:DATA?",
            delimiter=b"\n\n",
            binary=True,
            block=block,
            callback=handle_waveform_data,
            error_callback=error_callback,
        )
        if block and type(data) == bytes and len(data) > 2:
            # Convert bytes to y axis data
            data = np.frombuffer(
                data[:-2], dtype=(np.int16 if self._waveform_width == 16 else np.int8)
            )
            data = (
                data * (self.wfp["vertical_gain"] / self.wfp["code_per_div"])
                - self.wfp["vertical_offset"]
            )
            # Create time axis
            time = (
                self.wfp["horizontal_offset"]
                - (self.wfp["time_base"] * self._waveform_grid / 2)
                + np.arange(
                    start=self.wfp["wave_array_start"],
                    stop=self.wfp["wave_array_start"]
                    + (
                        min(self.wfp["wave_array_points"], self.wfp["chunk_size_max"])
                        * self.wfp["wave_array_interval"]
                    ),
                    step=self.wfp["wave_array_interval"],
                    dtype=self.waveform_time_dtype,
                )
                * self.wfp["horizontal_interval"]
            )
            return time, data

    def get_waveforms(self, channels=("C1",), block=True, callback=None):
        """
        Get all requested waveforms using multiple data acquisition requests.

        The ``channels`` parameter specifies the channels to retrieve waveform data for. Valid
        channel specifications are listed in the :attr:`~siglent_sds.utils.waveform_sources` array,
        but note that not all sources are available on every model of oscilloscope. Analog channels
        are specified using the form ``"C1"``, ``"C2"``, ``"C3"``, ``"C4"``. Math function channels
        are specified using ``"F1"``, ``"F2"`` etc. Lists of channels may be specified using any of
        the methods accepted by the :func:`~siglent_sds.utils.parse_channel_list` utility function.

        The ``callback`` parameter should provide a function to call when the acquired data is
        ready. It should take the form of ``callback(channels, time, data)``.

        A list of labels for the acquired channels will be returned as the ``channels`` parameter.

        The waveform time axis will be provided as a 1D numpy array of the same length as the last
        ``data`` axis as the ``time`` parameter. It contains the time values corresponding to the
        waveform points, in seconds.

        The returned ``data`` will be a single multi-dimensional numpy array. The returned array
        will have shape [`channel_i`, `sequence_i`, `point_i`], where `channel_i` is the channel
        index, `sequence_i` is the waveform sequence index, and `point_i` is the waveform point
        index. Note that even if sequence mode is disabled, the array will still contain the
        sequence axis with length 1. Similarly, even if only a single channel is specified, the
        array will still contain the channel axis. Values in the data array are the point values in
        volts. The :func:`numpy.squeeze` function can be used to remove the redundant axes.

        :param channels: List of channels to acquire from.
        :param callback: Function to call with acquired data.
        """
        # Holders for return data for when blocking behaviour used
        global gwf_time
        global gwf_data
        # global gwf_exception
        gwf_time = None
        gwf_data = None
        # gwf_exception = None

        if block:
            self._unblock.clear()

        # Handle different forms of channel parameter
        channels = parse_channel_list(channels)

        def handle_waveforms(data_array, channel_i, n_channels, chunk_i, n_chunks, data):
            """
            Handler for waveform data. Insert chunk into data_array, do callback once complete.
            """
            # Empty data will still contain the two \n termination characters
            if len(data) <= 2:
                self._log.debug(
                    f"No data received for waveform chunk {chunk_i} request for channel {channel_i}."
                )
            else:
                data = np.frombuffer(
                    data[:-2], dtype=(np.int16 if self._waveform_width == 16 else np.int8)
                )
                data = (
                    data * (self.wfp["vertical_gain"] / self.wfp["code_per_div"])
                    - self.wfp["vertical_offset"]
                )
                self._log.debug(
                    f"Received waveform chunk {chunk_i+1}/{n_chunks} for channel index {channel_i+1}/{n_channels}, length = {len(data)} points."
                )
                # If data comes from a math function channel we always get the full waveform and the
                # start, points, interval parameters aren't respected. We also don't get sequence
                # data, and just a single waveform. If that's the case, trim down to fit in the data
                # array. The sequence data for waveforms other than the first will be NaN for any
                # math function channels.
                if channels[channel_i].startswith("F"):
                    # Could be full size math function data
                    # self._log.debug(f"Function channel data, trimming to {self.wfp["wave_array_points"]} points.")
                    start_i = max(1, self.wfp["wave_array_start"]) - 1
                    stop_i = start_i + (
                        self.wfp["wave_array_points"] * self.wfp["wave_array_interval"]
                    )
                    step = self.wfp["wave_array_interval"]
                    data = data[start_i:stop_i:step]
                col_lo = chunk_i * self.wfp["chunk_size_max"]
                col_hi = col_lo + len(data)
                data_array[channel_i, col_lo:col_hi] = data
            # Check if we're done making waveform data requests
            if (channel_i + 1 == len(channels)) and (chunk_i + 1 == n_chunks):
                global gwf_time
                global gwf_data
                # We should have collected data for all requested channels. There's possibly sequence data
                # that has been collected, so we reshape the numpy array to be (channel, sequence, point).
                gwf_data = data_array.reshape((len(channels), -1, self.wfp["wave_array_points"]))
                # Compute a time axis which should be valid for all channels and sequence waveforms
                start_i = self.wfp["wave_array_start"] - chunk_i * self.wfp["chunk_size_max"]
                stop_i = start_i + (self.wfp["wave_array_points"] * self.wfp["wave_array_interval"])
                gwf_time = (
                    self.wfp["horizontal_offset"]
                    - (self.wfp["time_base"] * self._waveform_grid / 2)
                    + np.arange(
                        start=start_i,
                        stop=stop_i,
                        step=self.wfp["wave_array_interval"],
                        dtype=np.float64,
                    )
                    * self.wfp["horizontal_interval"]
                )
                # Cast to desired precision
                gwf_time = gwf_time.astype(self.waveform_time_dtype)
                # Done, pass time axis and data array to callback function
                if callable(callback):
                    callback(channels, gwf_time, gwf_data)
                else:
                    self._log.debug(
                        f"Waveform data received: (ch, seq, points) = {gwf_data.shape}, t = {gwf_time[0]:g} to {gwf_time[-1]:g}."
                    )
                # Unblock now we've finished acquiring chunks
                self._unblock.set()

        def queue_acquisitions():
            """
            Queue up the required series of acquisitions of data chunks for the requested waveforms.
            """
            # Allocate the buffer we'll need to store the full waveform data. This can be multiple
            # channels which will be in the rows of the array, and multiple waveforms in the sequence
            # which will be stored end-to-end within a row.
            # self._log.debug(f"Allocating data array for shape ({len(channels)}, {self.wfp['frames_sum']}, {self.wfp['wave_array_points']})")
            data_array = np.full(
                (len(channels), self.wfp["frames_sum"] * self.wfp["wave_array_points"]),
                np.nan,
                dtype=self.waveform_data_dtype,
            )
            # Calculate the number of chunks we need to read the complete waveform/sequence
            n_chunks = int(
                np.ceil(
                    self.wfp["wave_array_points"]
                    * self.wfp["frames_sum"]
                    / self.wfp["chunk_size_max"]
                )
            )
            # Configure to return multiple waveforms in sequence within each chunk
            self.send(":WAV:SEQ 0,1", delimiter=b"", block=False)
            # Remember the current wave_array_start setting
            wave_array_start_orig = self.wfp["wave_array_start"]
            # Loop through the requested channels
            for channel_i, channel in enumerate(channels):
                # Select the channel
                self.send(f":WAV:SOUR {channel}", delimiter=b"", block=False)
                # Loop through number of chunks required for waveform (or sequence)
                for chunk_i in range(n_chunks):
                    # Get chunk data and stick it into data_array
                    self.update_waveform_preamble(block=False)
                    self.send(
                        ":WAV:DATA?",
                        delimiter=b"\n\n",
                        binary=True,
                        block=False,
                        callback=partial(
                            handle_waveforms,
                            data_array,
                            channel_i,
                            len(channels),
                            chunk_i,
                            n_chunks,
                        ),
                    )
                    if chunk_i + 1 < n_chunks:
                        # More chunks to go...
                        if self.wfp["wave_array_points"] > self.wfp["chunk_size_max"]:
                            # A single waveform is larger than a single chunk, increment starting
                            # data point
                            self.send(
                                f":WAV:STAR {wave_array_start_orig + (chunk_i + 1)*self.wfp['chunk_size_max']}",
                                delimiter=b"",
                                block=False,
                            )
                        else:
                            # Sequence mode, increment frame index. Note that sequence mode is not
                            # possible when waveform set to 10M points, so we won't ever need to
                            # handle that scenario.
                            self.send(
                                f":WAV:SEQ 0,{self.wfp['frames_sum'] - (n_chunks - chunk_i - 2)*self.wfp['frames_read']}",
                                delimiter=b"",
                                block=False,
                            )
                # Finished getting chunks for this channel, reset the original first point value
                self.send(f":WAV:STAR {wave_array_start_orig}", delimiter=b"", block=False)
                self.update_waveform_parameters(block=False)

        def handle_inr(data):
            """
            Handle the response from the INternal state Register (INR) request. Note that this
            command is undocumented for the SDS800X HD series, but seems to follow the documentation
            in the SDS1000 programming guide.
            """
            try:
                data = int(data.removeprefix(b"INR "))
            except Exception as ex:
                self._log.debug(f"Unable to interpret internal state register: {data}")
                # if callable(error_callback):
                #     error_callback(ex)
                self._unblock.set()
                return
            if data & 0x0001:
                # If INR bit 0 is set, a new waveform is ready
                self._log.debug(f"Retrieving new waveform data (INR={data}).")
                # Select first analog channel if any, so waveform parameters reflect analog and not function channel
                for ch in channels:
                    if ch.startswith("C"):
                        self.send(f":WAV:SOUR {ch}", delimiter=b"", block=False)
                        break
                # Ensure the waveform parameters are updated before retrieving any data
                self.update_waveform_parameters(
                    block=False, callback=lambda params: queue_acquisitions()
                )
            else:
                self._log.debug(f"No new waveform data available (INR={data}).")
                self._unblock.set()

        # Ask for internal state register to see if new waveform data is available
        self.send("INR?", callback=handle_inr, block=False)
        if block:
            if self._unblock.wait(self.get_waveforms_timeout):
                return channels, gwf_time, gwf_data
            else:
                raise TimeoutError("Timeout waiting for get_waveforms to complete.")

    def waveform_width(self, width, block=True, callback=None, error_callback=None):
        """
        Set the bit width of the returned waveform data. This should be set to 16 bit (WORD) when
        the ADC resolution is greater than 8 bits, such as on the SDS800X HD which uses 12-bit
        acquisition.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary.

        :param width: Bit width of response data, ``8`` or ``"BYTE"``, or ``16`` or ``"WORD"``.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        if type(width) == str:
            if width.upper() == "BYTE":
                width = "BYTE"
            else:
                width = "WORD"
        else:
            if width == 8:
                width = "BYTE"
            else:
                width = "WORD"
        self._waveform_width = 8 if width == "BYTE" else 16
        self.send(f":WAV:WIDT {width}", delimiter=b"", block=False, error_callback=error_callback)
        self.update_waveform_preamble(block=block, callback=callback, error_callback=error_callback)

    def waveform_source(self, source, block=True, callback=None, error_callback=None):
        """
        Configure the waveform source channel.

        The channels should be one of the analog channels, ``"C1"``, ``"C2"``, ``"C3"``, ``"C4"``,
        one of the math function channels, ``"F1"``, ``"F2"``, ``"F3"``, ``"F4"``, or one of the
        digital inputs, ``"Dn"``. The ``source`` parameter can also be specified as an integer,
        where the analog channels start from 0, and the function channels start from 8.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary.

        :param source: Source channel for waveform acquisition.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        if type(source) == int and (0 <= source < len(waveform_sources)):
            source = waveform_sources[source]
        self.send(f":WAV:SOUR {source}", delimiter=b"", block=False, error_callback=error_callback)
        self.update_waveform_preamble(block=block, callback=callback, error_callback=error_callback)

    def waveform_start(
        self, point_num=None, t=None, block=True, callback=None, error_callback=None
    ):
        """
        Configure the starting point to be returned from a :meth:`waveform_data` request.

        .. warning::

            Note that currently using a non-zero starting point in sequence mode is broken, at least
            on the SDS800X HD and possibly other "HD" devices that use 12-bit or greater sampling
            resolution. This seems like an issue with the way the devices return multi-waveform
            data. This may need to wait for a firmware fix, or possibly could be worked around by
            requesting each sequence waveform individually.

            If using sequence mode, consider if :meth:`timebase_delay` might be a suitable
            alternative.

        If the ``t`` parameter is specified as time in seconds relative to the trigger point zero,
        the value of ``point_num`` will be overridden with the data point calculated using the
        current time base.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary.

        :param point_num: Starting data point number to return in waveform requests.
        :param t: Starting time point to return in waveform requests, in seconds.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        if not t is None:
            # Convert time point to point number using current timebase
            try:
                point_num = (
                    self.wfp["wave_array_max"] // 2 + int(t / self.wfp["horizontal_interval"]) - 1
                )
            except:
                pass
        if point_num is None:
            # Set to first point
            point_num = 0
        if point_num >= self.wfp["wave_array_max"]:
            point_num = self.wfp["wave_array_max"] - 1
        elif point_num < 0:
            point_num = 0

        self.send(
            f":WAV:STAR {point_num}", delimiter=b"", block=False, error_callback=error_callback
        )
        self.update_waveform_preamble(
            block=block, callback=callback, error_callback=error_callback
        )

    def waveform_points(
        self, num_points=None, t=None, block=True, callback=None, error_callback=None
    ):
        """
        Configure the number of waveform points to be returned from a :meth:`waveform_data` request.

        If the ``t`` parameter is specified as time in seconds, the value of ``num_points`` will be
        overridden with the number of data points calculated using the current time base and data
        point interval. Note that if the time interval is subsequently changed using
        :meth:`waveform_interval` then the number of returned points will no longer be equivalent to
        the given time window.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary.

        :param num_points: Number of data points to return in waveform requests.
        :param t: Time interval to return in waveform requests, in seconds.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        if not t is None:
            # Convert time window to number of points using current timebase
            try:
                num_points = int(
                    0.5 + t / (self.wfp["horizontal_interval"] * self.wfp["wave_array_interval"])
                )
            except:
                pass
        if num_points is None or num_points <= 0:
            # This should set to max points
            num_points = self.wfp["wave_array_max"]
        # Limit to possible number of points considering current start and interval
        num_points = min(
            num_points,
            (self.wfp["wave_array_max"] - self.wfp["wave_array_start"])
            // self.wfp["wave_array_interval"],
        )

        self.send(
            f":WAV:POIN {num_points}", delimiter=b"", block=False, error_callback=error_callback
        )
        self.update_waveform_preamble(
            block=block, callback=callback, error_callback=error_callback
        )

    def waveform_interval(
        self, num_points=None, t=None, block=True, callback=None, error_callback=None
    ):
        """
        Configure the interval between points returned from a :meth:`waveform_data` request.

        If the ``t`` parameter is specified as time in seconds, the value of ``num_points`` will be
        overridden with the number of data points calculated using the current time base.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary.

        :param num_points: Interval between data points to return in waveform requests.
        :param t: Time interval between data points to return in waveform requests, in seconds.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        if not t is None:
            # Convert time interval to number of points using current timebase
            try:
                num_points = int(t / self.wfp["horizontal_interval"])
            except:
                pass
        if num_points is None:
            # Set to return every data point
            num_points = 1

        self.send(
            f":WAV:INT {num_points}", delimiter=b"", block=False, error_callback=error_callback
        )
        self.update_waveform_preamble(
            block=block, callback=callback, error_callback=error_callback
        )

    def timebase_delay(self, delay=0.0, block=True, callback=None, error_callback=None):
        """
        Set the main timebase delay between the trigger event and the delay reference point.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary, where the ``"horizontal_offset"`` entry
        should be the value of the new timebase delay.

        :param delay: Time delay between trigger event and delay reference point, in seconds.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f":TIM:DEL {delay}",
            delimiter=b"",
            wait=0.001,
            block=False,
            callback=callback,
            error_callback=error_callback,
        )
        self.update_waveform_parameters(
            block=block, callback=callback, error_callback=error_callback
        )

    def timebase_scale(self, scale=1e-3, block=True, callback=None, error_callback=None):
        """
        Set the main timebase scale per division.

        The value of the ``scale`` parameter needs to be valid for the particular model of the
        oscilloscope. Possible values are listed in the :data:`~siglent_sds.utils.timebase_values` list.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary, where the ``"time_base"`` entry should be
        the value of the new timebase scale.

        :param scale: Time scale per division.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f":TIM:SCAL {scale}",
            delimiter=b"",
            wait=0.001,
            block=False,
            callback=callback,
            error_callback=error_callback,
        )
        self.update_waveform_parameters(
            block=block, callback=callback, error_callback=error_callback
        )

    def channel_switch(self, channel=1, state=True, block=True, callback=None, error_callback=None):
        """
        Turn the specified analog channel off or on.

        Note that updating the waveform preamble data with :meth:`update_waveform_preamble` or
        :meth:`update_waveform_parameters` will have the side effect of enabling the channel last
        selected by :meth:`waveform_source`.

        :param channel: Channel number, numbered from 1.
        :param state: Boolean state of the channel.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f"CHAN{channel}:SWIT {'ON' if state else 'OFF'}",
            delimiter=b"",
            block=block,
            callback=callback,
            error_callback=error_callback,
        )

    def channels_enabled(self, channels="", block=True, callback=None, error_callback=None):
        """
        Enable the specified channels, and disable those not listed.

        The channel selection may be anything accepted by the
        :func:`~siglent_sds.utils.parse_channel_list` utility function.

        Note that updating the waveform preamble data with :meth:`update_waveform_preamble` or
        :meth:`update_waveform_parameters` will have the side effect of enabling the channel last
        selected by :meth:`waveform_source`.

        :param channels: List of channels to enable.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        channels = parse_channel_list(channels)
        for ch_i in range(1, self._analog_channels + 1):
            self.send(
                f"CHAN{ch_i}:SWIT {'ON' if f'C{ch_i}' in channels else 'OFF'}",
                delimiter=b"",
                block=False,
                error_callback=error_callback,
            )
        self.wait(0.5, block=block, callback=callback, error_callback=error_callback)

    def channel_visible(
        self, channel=1, state=True, block=True, callback=None, error_callback=None
    ):
        """
        Turn the visibility of the specified analog channel off or on.

        Visibility is different to enabling the channel. An invisible channel will still acquire
        data, but won't be displayed on the screen of the device.

        :param channel: Channel number, numbered from 1.
        :param state: Boolean visibility state of the channel.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f"CHAN{channel}:VIS {'ON' if state else 'OFF'}",
            delimiter=b"",
            block=block,
            callback=callback,
            error_callback=error_callback,
        )

    def channels_visible(self, channels="", block=True, callback=None, error_callback=None):
        """
        Make the specified channels visible, and hide those not listed.

        Visibility is different to enabling the channel. An invisible channel will still acquire
        data, but won't be displayed on the screen of the device.

        The channel selection may be anything accepted by the
        :func:`~siglent_sds.utils.parse_channel_list` utility function.

        :param channels: List of channels to enable.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        channels = parse_channel_list(channels)
        for ch_i in range(1, self._analog_channels + 1):
            self.send(
                f"CHAN{ch_i}:VIS {'ON' if f'C{ch_i}' in channels else 'OFF'}",
                delimiter=b"",
                block=(False if ch_i < self._analog_channels else block),
                error_callback=error_callback,
            )

    def channel_scale(
        self,
        channel=1,
        scale=1.0,
        offset=None,
        skew=None,
        block=True,
        callback=None,
        error_callback=None,
    ):
        """
        Set the vertical sensitivity for an analog channel in volts per division, and optionally the
        offset and skew.

        :param channel: Channel number, numbered from 1.
        :param scale: Vertical sensitivity in volts per division.
        :param offset: Vertical offset in volts.
        :param offset: Horizontal offset in seconds.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(f"CHAN{channel}:SCAL {scale}", delimiter=b"", block=False, wait=0.01)
        if not offset is None:
            self.send(f"CHAN{channel}:OFFS {offset}", delimiter=b"", block=False, wait=0.01)
        if not skew is None:
            self.send(f"CHAN{channel}:SKEW {skew}", delimiter=b"", block=False)
        self.wait(0.5, block=block, callback=callback, error_callback=error_callback)

    def channel_offset(self, channel=1, offset=0.0, block=True, callback=None, error_callback=None):
        """
        Set the vertical offset for an analog channel in volts.

        :param channel: Channel number, numbered from 1.
        :param offset: Vertical offset in volts.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f"CHAN{channel}:OFFS {offset}",
            delimiter=b"",
            block=block,
            callback=callback,
            error_callback=error_callback,
        )

    def channel_skew(self, channel=1, skew=0.0, block=True, callback=None, error_callback=None):
        """
        Set the horizontal skew for an analog channel in seconds.

        :param channel: Channel number, numbered from 1.
        :param offset: Horizontal offset in seconds.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(
            f"CHAN{channel}:SKEW {skew}",
            delimiter=b"",
            block=block,
            callback=callback,
            error_callback=error_callback,
        )

    def sequence(self, seq=True, block=True, callback=None, error_callback=None):
        """
        Enable or disable sequence mode, or set the number of waveform acquisitions in sequence
        mode.

        If the parameter is 1 or less, sequence mode will be disabled without changing the value.
        For values greater than one, sequence mode will be enabled automatically.

        Sequence mode can also be enabled or disabled without changing the number of acquisitions in
        the sequence by passing ``True`` or ``False``, respectively.

        .. warning::

            Currently, using sequence mode in combination with :meth:`waveform_start` is likely
            broken. See the note in the documentation for :meth:`waveform_start` for possible
            workarounds.

        :param seq: Number of waveform acquisitions in the sequence, or True or False.
        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        if type(seq) == int and seq > 1:
            self.send(
                f"ACQ:SEQ:COUN {seq}",
                delimiter=b"",
                block=False,
            )
            self.send("ACQ:SEQ ON", delimiter=b"", block=False)
        elif type(seq) == int:
            self.send("ACQ:SEQ OFF", delimiter=b"", block=False)
        else:
            self.send(f"ACQ:SEQ {'ON' if seq else 'OFF'}", delimiter=b"", block=False)
        self.wait(0.1, block=block, callback=callback, error_callback=error_callback)

    def png(self, filename="sds_screenshot.png", block=True, callback=None, error_callback=None):
        """
        Take a screenshot of the device display and save it as a PNG image file.

        The filename can be set to ``None`` if the file should not be saved. The PNG image data will
        still be passed to any provided ``callback`` function, and returned from this method if the
        default ``block=True`` behaviour is used.

        If the ``callback`` parameter is used, it should take one parameter which will be the PNG
        image data.

        :param filename: Filename to use for the image file.
        :param block: Block function return until command completed.
        :param callback: Function to call once PNG data is ready.
        :param error_callback: Function to call if an error occurs.
        :returns: PNG image data if default ``block=True`` parameter used.
        """

        # TODO: Add timestamp to default filenames?
        def handle_png(data):
            try:
                if filename:
                    with open(filename, "wb") as f:
                        f.write(data[:-1])
                if callable(callback):
                    callback(data[:-1])
            except Exception as ex:
                error_callback(ex)

        # Delimiter is the PNG IEND chunk, plus a newline
        command_result = self.send(
            ":PRIN? PNG",
            delimiter=b"\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82\n",
            block=block,
            callback=handle_png,
            error_callback=error_callback,
        )
        if block and type(command_result) == bytes:
            return command_result[:-1]

    def autoset(self, block=True, callback=None, error_callback=None):
        """
        Run the autoset routine to select appropriate parameters for the waveform.

        If the ``callback`` parameter is used, the callback function should accept one parameter
        which will be the updated :data:`wfp` dictionary.

        :param block: Block function return until command completed.
        :param callback: Function to call once command has completed.
        :param error_callback: Function to call if an error occurs.
        """
        self.send(":AUT", delimiter=b"", block=False, error_callback=error_callback)
        # The device won't respond until the autoset procedure is complete, about 4 seconds
        self.wait(4.0, block=block)
        self.update_waveform_preamble(block=block, callback=callback, error_callback=error_callback)
