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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .user_defined_child import user_defined_child


class user_defined(NamedObject[user_defined_child], CreatableNamedObjectMixinOld[user_defined_child]):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: user_defined_child = user_defined_child
    """
    child_object_type of user_defined.
    """
    return_type = "<object object at 0x7f641d662030>"
