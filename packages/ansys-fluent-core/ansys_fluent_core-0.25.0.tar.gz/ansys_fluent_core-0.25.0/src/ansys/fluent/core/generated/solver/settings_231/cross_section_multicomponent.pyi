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

from .cross_section_multicomponent_child import cross_section_multicomponent_child


class cross_section_multicomponent(NamedObject[cross_section_multicomponent_child], _NonCreatableNamedObjectMixin[cross_section_multicomponent_child]):
    fluent_name = ...
    child_object_type: cross_section_multicomponent_child = ...
    return_type = ...
