"""
This module contains classes specific to particular device models. They will initialise
:class:`~siglent_sds.base.SDS_Base` with the appropriate values for the ``analog_channels``,
``waveform_width``, and ``waveform_grid`` parameters. In the future these may also perform some
other custom behaviour specific to the model.

There are also generic classes for 2-channel and 4-channel devices (:class:`SDS_2ch` and
:class:`SDS_4ch`). The "HD" variants are for models with 12-bit ADCs (:class:`SDS_2ch_HD` and
:class:`SDS_4ch_HD`).

All the classes here are imported into the main namespace, and thus can be used with something like 

.. code-block::python

    from siglent_sds import SDS_4ch_HD sds = SDS_4ch_HD(host=127.0.0.1)  # Change to correct IP
    address! # ...
"""

from .base import SDS_Base


class SDS_2ch(SDS_Base):
    """
    Generic two-channel 8-bit standard model.
    """

    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=8, waveform_grid=10, **kwargs)


class SDS_4ch(SDS_Base):
    """
    Generic four-channel 8-bit standard model.
    """

    def __init__(self, **kwargs):
        super().__init__(analog_channels=4, waveform_width=8, waveform_grid=10, **kwargs)


class SDS_2ch_HD(SDS_Base):
    """
    Generic two-channel 12-bit HD model.
    """

    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=16, waveform_grid=10, **kwargs)


class SDS_4ch_HD(SDS_Base):
    """
    Generic four-channel 12-bit HD model.
    """

    def __init__(self, **kwargs):
        super().__init__(analog_channels=4, waveform_width=16, waveform_grid=10, **kwargs)


# SDS800X HD have 12-bit ADC, use waveform_width=16
class SDS802X_HD(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=16, waveform_grid=10, **kwargs)


class SDS804X_HD(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=4, waveform_width=16, waveform_grid=10, **kwargs)


class SDS812X_HD(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=16, waveform_grid=10, **kwargs)


class SDS814X_HD(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=4, waveform_width=16, waveform_grid=10, **kwargs)


class SDS822X_HD(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=16, waveform_grid=10, **kwargs)


class SDS824X_HD(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=4, waveform_width=16, waveform_grid=10, **kwargs)


# SHS800X and SHS1000X should have waveform_grid=12
class SHS810X(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=8, waveform_grid=12, **kwargs)


class SHS820X(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=8, waveform_grid=12, **kwargs)


class SHS1102X(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=8, waveform_grid=12, **kwargs)


class SHS1202X(SDS_Base):
    def __init__(self, **kwargs):
        super().__init__(analog_channels=2, waveform_width=8, waveform_grid=12, **kwargs)
