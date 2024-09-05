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

from typing import Union, List, Tuple

from .user_defined_child import user_defined_child


class user_defined(NamedObject[user_defined_child], CreatableNamedObjectMixinOld[user_defined_child]):
    fluent_name = ...
    child_object_type: user_defined_child = ...
    return_type = ...
