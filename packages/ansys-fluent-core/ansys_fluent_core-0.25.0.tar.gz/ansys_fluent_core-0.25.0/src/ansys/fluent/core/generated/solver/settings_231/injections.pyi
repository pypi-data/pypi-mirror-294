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

from .injections_child import injections_child


class injections(NamedObject[injections_child], CreatableNamedObjectMixinOld[injections_child]):
    fluent_name = ...
    child_object_type: injections_child = ...
    return_type = ...
