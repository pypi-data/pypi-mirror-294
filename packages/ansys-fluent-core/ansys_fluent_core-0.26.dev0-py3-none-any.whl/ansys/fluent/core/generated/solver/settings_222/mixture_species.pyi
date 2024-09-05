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

from .fluid_child import fluid_child


class mixture_species(NamedObject[fluid_child], CreatableNamedObjectMixinOld[fluid_child]):
    fluent_name = ...
    child_object_type: fluid_child = ...
    return_type = ...
