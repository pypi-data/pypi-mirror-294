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

from .child_object_type_child import child_object_type_child


class tss_scalar(NamedObject[child_object_type_child], CreatableNamedObjectMixinOld[child_object_type_child]):
    """
    'tss_scalar' child.
    """

    fluent_name = "tss-scalar"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of tss_scalar.
    """
    return_type = "<object object at 0x7f570335d930>"
