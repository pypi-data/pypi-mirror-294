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

from .user_defined_child import user_defined_child


class user_defined(NamedObject[user_defined_child], CreatableNamedObjectMixinOld[user_defined_child]):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    child_object_type: user_defined_child = user_defined_child
    """
    child_object_type of user_defined.
    """
    return_type = "<object object at 0x7f115b6a8f40>"
