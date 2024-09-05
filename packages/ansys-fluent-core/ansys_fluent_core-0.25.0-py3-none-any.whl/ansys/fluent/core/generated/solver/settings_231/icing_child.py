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

from .report_type import report_type as report_type_cls
from .old_props import old_props as old_props_cls

class icing_child(Group):
    """
    'child_object_type' of icing.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['report_type', 'old_props']

    _child_classes = dict(
        report_type=report_type_cls,
        old_props=old_props_cls,
    )

    return_type = "<object object at 0x7f115b6a9070>"
