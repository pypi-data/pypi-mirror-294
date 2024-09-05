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

from .enabled_57 import enabled as enabled_cls

class enable(Command):
    """
    Enable/Disable transient postprocessing?.
    
    Parameters
    ----------
        enabled : bool
            Enable/Disable transient postprocessing?.
    
    """

    fluent_name = "enable"

    argument_names = \
        ['enabled']

    _child_classes = dict(
        enabled=enabled_cls,
    )

