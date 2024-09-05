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

from .amg_gpgpu_options_child import amg_gpgpu_options_child


class amg_gpgpu_options(NamedObject[amg_gpgpu_options_child], _NonCreatableNamedObjectMixin[amg_gpgpu_options_child]):
    fluent_name = ...
    child_object_type: amg_gpgpu_options_child = ...
    return_type = ...
