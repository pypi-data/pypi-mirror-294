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

from .porous_jump_child import porous_jump_child


class porous_jump(NamedObject[porous_jump_child], _NonCreatableNamedObjectMixin[porous_jump_child]):
    """
    'porous_jump' child.
    """

    fluent_name = "porous-jump"

    child_object_type: porous_jump_child = porous_jump_child
    """
    child_object_type of porous_jump.
    """
    return_type = "<object object at 0x7f115c9ff1f0>"
