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

from .global_range import global_range as global_range_cls

class auto_range_on(Group):
    """
    'auto_range_on' child.
    """

    fluent_name = "auto-range-on"

    child_names = \
        ['global_range']

    _child_classes = dict(
        global_range=global_range_cls,
    )

    return_type = "<object object at 0x7f5cfb9b7060>"
