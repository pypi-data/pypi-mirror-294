"""
Sub-package containing testing and example scripts for use of the siglet_sds python library.

The simplest example lets you manipulate the device from the interactive python REPL (run, evaluate,
print, loop). Run it from within the source directory like:

.. code-block:: none

    python -i siglent_sds/examples/sds_repl.py --host 127.0.0.1

where you need to substitute the IP address or hostname of your device instead of ``127.0.0.1``.
Note also the ``-i`` option to python that runs the script in interactive mode.

To run the graphical example, ensure you have the ``pyqtgraph`` and ``pyside6`` dependencies
installed. Then run from within the source directory like:

.. code-block:: none

    python siglent_sds/examples/sds_plot.py
"""