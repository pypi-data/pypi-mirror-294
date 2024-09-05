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

from .read_data import read_data as read_data_cls
from .write_data import write_data as write_data_cls

class interpolate(Group):
    """
    Enter the interpolate menu.
    """

    fluent_name = "interpolate"

    command_names = \
        ['read_data', 'write_data']

    _child_classes = dict(
        read_data=read_data_cls,
        write_data=write_data_cls,
    )

