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

from .list import list as list_cls
from .graphics_objects_child import graphics_objects_child


class graphics_objects(NamedObject[graphics_objects_child], CreatableNamedObjectMixinOld[graphics_objects_child]):
    """
    'graphics_objects' child.
    """

    fluent_name = "graphics-objects"

    command_names = \
        ['list']

    _child_classes = dict(
        list=list_cls,
    )

    child_object_type: graphics_objects_child = graphics_objects_child
    """
    child_object_type of graphics_objects.
    """
    return_type = "<object object at 0x7f115b5a2ca0>"
