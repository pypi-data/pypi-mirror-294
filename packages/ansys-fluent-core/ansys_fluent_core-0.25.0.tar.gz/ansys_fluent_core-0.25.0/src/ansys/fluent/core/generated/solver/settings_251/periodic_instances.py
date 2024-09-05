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

from .create_1 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .detect_surfaces import detect_surfaces as detect_surfaces_cls
from .clear_repeats import clear_repeats as clear_repeats_cls
from .periodic_instances_child import periodic_instances_child


class periodic_instances(NamedObject[periodic_instances_child], CreatableNamedObjectMixin[periodic_instances_child]):
    """
    Periodic instance objects are used to specify periodic repetition of surfaces.
    """

    fluent_name = "periodic-instances"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy', 'detect_surfaces', 'clear_repeats']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        detect_surfaces=detect_surfaces_cls,
        clear_repeats=clear_repeats_cls,
    )

    child_object_type: periodic_instances_child = periodic_instances_child
    """
    child_object_type of periodic_instances.
    """
