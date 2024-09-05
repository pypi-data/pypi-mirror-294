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

from .surface_child import surface_child


class surface(NamedObject[surface_child], CreatableNamedObjectMixinOld[surface_child]):
    """
    'surface' child.
    """

    fluent_name = "surface"

    child_object_type: surface_child = surface_child
    """
    child_object_type of surface.
    """
    return_type = "<object object at 0x7f57023d1f70>"
