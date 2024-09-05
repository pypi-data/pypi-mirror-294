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


class cross_section_multicomponent_child(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'child_object_type' of cross_section_multicomponent.
    """

    fluent_name = "child-object-type"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of cross_section_multicomponent_child.
    """
    return_type = "<object object at 0x7f115c1a67d0>"
