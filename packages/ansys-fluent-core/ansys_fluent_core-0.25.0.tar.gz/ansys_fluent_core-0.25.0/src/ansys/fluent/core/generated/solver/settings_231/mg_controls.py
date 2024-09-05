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

from .mg_controls_child import mg_controls_child


class mg_controls(NamedObject[mg_controls_child], _NonCreatableNamedObjectMixin[mg_controls_child]):
    """
    'mg_controls' child.
    """

    fluent_name = "mg-controls"

    child_object_type: mg_controls_child = mg_controls_child
    """
    child_object_type of mg_controls.
    """
    return_type = "<object object at 0x7f115b7b6c50>"
