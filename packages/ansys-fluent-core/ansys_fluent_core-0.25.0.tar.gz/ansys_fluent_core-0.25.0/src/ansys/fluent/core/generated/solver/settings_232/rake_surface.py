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
from .rake_surface_child import rake_surface_child


class rake_surface(NamedObject[rake_surface_child], CreatableNamedObjectMixinOld[rake_surface_child]):
    """
    'rake_surface' child.
    """

    fluent_name = "rake-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: rake_surface_child = rake_surface_child
    """
    child_object_type of rake_surface.
    """
    return_type = "<object object at 0x7f641d550f10>"
