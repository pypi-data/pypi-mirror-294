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

from .parameter_type import parameter_type as parameter_type_cls
from .entity_list import entity_list as entity_list_cls
from .individual_or_group import individual_or_group as individual_or_group_cls
from .individual_value import individual_value as individual_value_cls
from .group_value import group_value as group_value_cls
from .value_list import value_list as value_list_cls

class add_rom_parameter(Command):
    """
    'add_rom_parameter' command.
    
    Parameters
    ----------
        parameter_type : int
            'parameter_type' child.
        entity_list : List
            'entity_list' child.
        individual_or_group : bool
            'individual_or_group' child.
        individual_value : bool
            'individual_value' child.
        group_value : real
            'group_value' child.
        value_list : List
            'value_list' child.
    
    """

    fluent_name = "add-rom-parameter"

    argument_names = \
        ['parameter_type', 'entity_list', 'individual_or_group',
         'individual_value', 'group_value', 'value_list']

    _child_classes = dict(
        parameter_type=parameter_type_cls,
        entity_list=entity_list_cls,
        individual_or_group=individual_or_group_cls,
        individual_value=individual_value_cls,
        group_value=group_value_cls,
        value_list=value_list_cls,
    )

    return_type = "<object object at 0x7f5d0875d5d0>"
