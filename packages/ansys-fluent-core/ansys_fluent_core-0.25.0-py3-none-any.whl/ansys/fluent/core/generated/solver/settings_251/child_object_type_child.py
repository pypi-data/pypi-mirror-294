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

from .option_2 import option as option_cls
from .constant import constant as constant_cls
from .user_defined import user_defined as user_defined_cls

class child_object_type_child(Group):
    """
    'child_object_type' of child_object_type.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'constant', 'user_defined']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        user_defined=user_defined_cls,
    )

