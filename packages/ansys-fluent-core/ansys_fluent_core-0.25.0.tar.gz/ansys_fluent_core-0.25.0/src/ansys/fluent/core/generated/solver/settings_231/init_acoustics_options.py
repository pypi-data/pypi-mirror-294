#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .set_ramping_length import set_ramping_length as set_ramping_length_cls
from .time_step_count import time_step_count as time_step_count_cls

class init_acoustics_options(Command):
    """
    'init_acoustics_options' command.
    
    Parameters
    ----------
        set_ramping_length : bool
            Enable/Disable ramping length and initialize acoustics.
        time_step_count : int
            Set number of timesteps for ramping of sources.
    
    """

    fluent_name = "init-acoustics-options"

    argument_names = \
        ['set_ramping_length', 'time_step_count']

    _child_classes = dict(
        set_ramping_length=set_ramping_length_cls,
        time_step_count=time_step_count_cls,
    )

    return_type = "<object object at 0x7f115b6aa390>"
