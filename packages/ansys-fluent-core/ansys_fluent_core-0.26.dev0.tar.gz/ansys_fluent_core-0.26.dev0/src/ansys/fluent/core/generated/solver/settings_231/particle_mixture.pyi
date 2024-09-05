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

from .particle_mixture_child import particle_mixture_child


class particle_mixture(NamedObject[particle_mixture_child], CreatableNamedObjectMixinOld[particle_mixture_child]):
    fluent_name = ...
    child_object_type: particle_mixture_child = ...
    return_type = ...
