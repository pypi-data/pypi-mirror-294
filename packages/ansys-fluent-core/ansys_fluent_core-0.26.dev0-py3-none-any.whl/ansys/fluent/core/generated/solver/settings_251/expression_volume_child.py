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

from .name_2 import name as name_cls
from .expression_definition import expression_definition as expression_definition_cls
from .display_4 import display as display_cls

class expression_volume_child(Group):
    """
    'child_object_type' of expression_volume.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'expression_definition']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        expression_definition=expression_definition_cls,
        display=display_cls,
    )

