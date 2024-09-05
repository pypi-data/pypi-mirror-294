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

from .phase_child_20 import phase_child


class phase(NamedObject[phase_child], CreatableNamedObjectMixinOld[phase_child]):
    fluent_name = ...
    child_object_type: phase_child = ...
    return_type = ...
