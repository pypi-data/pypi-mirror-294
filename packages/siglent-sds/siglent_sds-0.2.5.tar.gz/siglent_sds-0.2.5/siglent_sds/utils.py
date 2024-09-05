import numpy as np


#: Table of parameters and their data types to be found in the waveform preamble data block.
_wave_descriptor_format = {
    "reserved_descriptor_name": "16s",
    "reserved_template_name": "16s",
    "reserved_comm_type": "H",
    "reserved_comm_order": "H",
    "reserved_descriptor_length": "L",
    "reserved_40_59": "20s",
    "reserved_wave_array_bytes": "L",
    "reserved_64_75": "12s",
    "reserved_instrument_name": "16s",
    "reserved_92_95": "4s",
    "reserved_96_111": "16s",
    "reserved_112_115": "4s",
    "wave_array_max": "L",
    "reserved_120_131": "12s",
    "wave_array_start": "L",
    "wave_array_interval": "L",
    "reserved_140_143": "4s",
    "frames_read": "L",
    "frames_sum": "L",
    "reserved_152_155": "4s",
    "vertical_gain": "f",
    "vertical_offset": "f",
    "code_per_div": "f",
    "reserved_168_171": "4s",
    "reserved_adc_bit": "H",
    "frames_index": "H",
    "horizontal_interval": "f",
    "horizontal_offset": "d",
    "reserved_188_195": "8s",
    "reserved_196_243": "48s",
    "reserved_244_291": "48s",
    "reserved_292_295": "4s",
    "reserved_296_311": "16s",
    "reserved_312_315": "4s",
    "reserved_316_323": "8s",
    "time_base": "H",
    "reserved_vertical_coupling": "H",
    "probe_attenuation": "f",
    "reserved_fixed_vertical_gain": "H",
    "bandwidth_limit": "H",
    "reserved_336_343": "8s",
    "wave_source": "H",
}
#: The waveform descriptor string used by :meth:`struct.unpack()` to decode the data block.
_wave_descriptor_format_string = "<" + "".join(_wave_descriptor_format.values())

#: List of timebase values which are available on the device, in seconds.
timebase_values = [
    200e-12,
    500e-12,
    1e-9,
    2e-9,
    5e-9,
    10e-9,
    20e-9,
    50e-9,
    100e-9,
    200e-9,
    500e-9,
    1e-6,
    2e-6,
    5e-6,
    10e-6,
    20e-6,
    50e-6,
    100e-6,
    200e-6,
    500e-6,
    1e-3,
    2e-3,
    5e-3,
    10e-3,
    20e-3,
    50e-3,
    100e-3,
    200e-3,
    500e-3,
    1,
    2,
    5,
    10,
    20,
    50,
    100,
    200,
    500,
    1000,
]

#: Names of the timebase values used when sending commands to the device.
timebase_names = [
    "200PS",
    "500PS",
    "1NS",
    "2NS",
    "5NS",
    "10NS",
    "20NS",
    "50NS",
    "100NS",
    "200NS",
    "500NS",
    "1US",
    "2US",
    "5US",
    "10US",
    "20US",
    "50US",
    "100US",
    "200US",
    "500US",
    "1MS",
    "2MS",
    "5MS",
    "10MS",
    "20MS",
    "50MS",
    "100MS",
    "200MS",
    "500MS",
    "1S",
    "2S",
    "5S",
    "10S",
    "20S",
    "50S",
    "100S",
    "200S",
    "500S",
    "1000S",
]

#: Waveform sources which can be requested from the device. Analog channels, math function channels, or digital channels.
waveform_sources = [
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "C7",
    "C8",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
    "D6",
    "D7",
    "D8",
    "D9",
    "D10",
    "D11",
    "D12",
    "D13",
    "D14",
    "D15",
    "D16",
]

def parse_channel_list(channels):
    """
    Utility to generate a list of channel specifiers from a variety of inputs.

    Valid forms of the ``channels`` parameter are:
    
    - Strings separated by spaces and/or commas such as ``"C1"`` or ``"C1,C2 C3"``.
    - A single integer which is interpreted as an analog channel number, such as ``1``.
    - A list of integers which are interpreted as analog channel numbers, such as ``[1, 2, 3]``.
    - A list of channel strings such as ``["C1", "C2", "C3"]``.

    Channels which are not listed in :attr:`waveform_sources` will be removed.

    :param channels: Channel list specifier.
    :returns: List of specified channels.
    """
    # Handle different forms of channel parameter
    if type(channels) == str:
        # Split string on comma or whitespace
        channels = [ch for ch in channels.replace(",", " ").split()]
    if type(channels) == int:
        # Convert single integer to list of one channel string
        channels = [f"C{channels}"]
    # Convert list of ints to list of channel strings
    channels = [f"C{ch}" if type(ch) == int else ch for ch in channels]
    # Convert channel names to uppercase
    channels = [ch.upper() for ch in channels]
    # Filter out obviously invalid channel names
    channels = [ch for ch in channels if ch in waveform_sources]
    return channels