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

from .force_child import force_child


class lift(NamedObject[force_child], CreatableNamedObjectMixinOld[force_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    child_object_type: force_child = force_child
    """
    child_object_type of lift.
    """
    return_type = "<object object at 0x7f115b6a8a20>"
