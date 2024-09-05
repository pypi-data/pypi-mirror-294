#!/usr/bin/env -S python -i

"""
Script to set up a :class:`SDS_Socket` object and interact with it using the python REPL.
"""

if __name__ == "__main__":

    import os
    import sys
    import logging
    import atexit

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

    logging.basicConfig(level=(logging.DEBUG if "--debug" in sys.argv else logging.INFO))
    try:
        host = sys.argv[sys.argv.index("--host") + 1]
    except:
        print("WARNING: the default host IP address will likely be incorrect!")
        print("Usage:")
        print(f"{sys.argv[0]} --host <hostname>")
        host = "10.42.0.59"

    #: An instance of the :class:`~siglent_sds.SDS_Base` class.
    sds = SDS_Base(host=host)
    atexit.register(sds.close)
    print(80 * "-")
    print("Send commands to the Siglent SDS oscilloscope using the sds object. For example:")
    print(">>> sds.autoset()")
    print(">>> sds.run()")
    print(">>> sds.png()")
    print("Custom commands (that don't expect a response) can be sent like:")
    print('>>> sds.command("*RST")')
    print("Custom queries are commands that expect a response, such as:")
    print('>>> sds.print_query(":ACQ:POIN?")')
    print("1.00E+06")
    print(80 * "-")
