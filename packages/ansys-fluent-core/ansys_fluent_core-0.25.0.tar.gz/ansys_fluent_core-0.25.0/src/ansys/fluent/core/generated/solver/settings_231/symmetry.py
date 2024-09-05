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

from .axis_child import axis_child


class symmetry(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'symmetry' child.
    """

    fluent_name = "symmetry"

    child_object_type: axis_child = axis_child
    """
    child_object_type of symmetry.
    """
    return_type = "<object object at 0x7f115bc7dd90>"
