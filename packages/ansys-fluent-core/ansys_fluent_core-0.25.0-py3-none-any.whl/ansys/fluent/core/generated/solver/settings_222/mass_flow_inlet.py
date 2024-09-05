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

from .change_type import change_type as change_type_cls
from .mass_flow_inlet_child import mass_flow_inlet_child


class mass_flow_inlet(NamedObject[mass_flow_inlet_child], CreatableNamedObjectMixinOld[mass_flow_inlet_child]):
    """
    'mass_flow_inlet' child.
    """

    fluent_name = "mass-flow-inlet"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_inlet.
    """
    return_type = "<object object at 0x7f57030d3690>"
