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


class mass_flow_multiplier(NamedObject[child_object_type_child], CreatableNamedObjectMixinOld[child_object_type_child]):
    """
    'mass_flow_multiplier' child.
    """

    fluent_name = "mass-flow-multiplier"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of mass_flow_multiplier.
    """
    return_type = "<object object at 0x7f5702767280>"
