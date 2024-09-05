Siglent_SDS
===========

Siglent_SDS is a python interface to Siglent oscilloscopes. It has been tested on the Siglent
SDS800X HD series, but may also be compatible with similar Siglent oscilloscope models such as:

- Siglent SDS5000X
- Siglent SDS2000X Plus
- Siglent SDS6000 Pro
- Siglent SDS6000A
- Siglent SHS800X
- Siglent SHS1000X
- Siglent SDS2000X HD
- Siglent SDS6000L
- Siglent SDS1000X HD
- Siglent SDS7000A
- Siglent SDS3000X HD

The interface attempts to follow the specification in the [Siglent SDS Programming
Guide](https://siglentna.com/download/29924/?tmstv=1722402666).

It is intended to simplify configuring and acquiring waveforms from the device. Currently the only supported connection type is through network sockets (ethernet), but USB or other connection backends could be added with relatively little effort. When using network sockets, there is no dependency on VISA libraries or similar.

Documentation is located at https://ptapping.gitlab.io/siglent_sds

Source code is located at https://gitlab.com/ptapping/siglent_sds

Python Package Index (PyPI) page at https://pypi.org/project/siglent-sds