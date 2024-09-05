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

from .timesteps import timesteps as timesteps_cls

class timestep_list(Command):
    """
    Select a list of timesteps.
    
    Parameters
    ----------
        timesteps : List
            Select a list of timesteps.
    
    """

    fluent_name = "timestep-list"

    argument_names = \
        ['timesteps']

    _child_classes = dict(
        timesteps=timesteps_cls,
    )

