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

from .multicomponent_child import multicomponent_child


class multicomponent(NamedObject[multicomponent_child], _NonCreatableNamedObjectMixin[multicomponent_child]):
    """
    'multicomponent' child.
    """

    fluent_name = "multicomponent"

    child_object_type: multicomponent_child = multicomponent_child
    """
    child_object_type of multicomponent.
    """
    return_type = "<object object at 0x7f115c1a5780>"
