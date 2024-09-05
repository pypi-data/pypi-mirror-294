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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .ungroup import ungroup as ungroup_cls
from .group_surface_child import group_surface_child


class group_surface(NamedObject[group_surface_child], _NonCreatableNamedObjectMixin[group_surface_child]):
    """
    Provides access to creating new group and ungroup existing surfaces.
    """

    fluent_name = "group-surface"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'ungroup']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        ungroup=ungroup_cls,
    )

    child_object_type: group_surface_child = group_surface_child
    """
    child_object_type of group_surface.
    """
