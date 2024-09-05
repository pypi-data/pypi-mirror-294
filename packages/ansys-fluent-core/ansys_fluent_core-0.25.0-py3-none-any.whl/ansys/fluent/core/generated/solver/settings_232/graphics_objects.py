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
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .graphics_objects_child import graphics_objects_child


class graphics_objects(NamedObject[graphics_objects_child], CreatableNamedObjectMixinOld[graphics_objects_child]):
    """
    'graphics_objects' child.
    """

    fluent_name = "graphics-objects"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: graphics_objects_child = graphics_objects_child
    """
    child_object_type of graphics_objects.
    """
    return_type = "<object object at 0x7f641d439e10>"
