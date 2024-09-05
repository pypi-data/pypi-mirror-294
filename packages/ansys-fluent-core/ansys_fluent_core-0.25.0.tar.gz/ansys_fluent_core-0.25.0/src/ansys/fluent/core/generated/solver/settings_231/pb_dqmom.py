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

from .child_object_type_child_1 import child_object_type_child


class pb_dqmom(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'pb_dqmom' child.
    """

    fluent_name = "pb-dqmom"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of pb_dqmom.
    """
    return_type = "<object object at 0x7f115c791a80>"
