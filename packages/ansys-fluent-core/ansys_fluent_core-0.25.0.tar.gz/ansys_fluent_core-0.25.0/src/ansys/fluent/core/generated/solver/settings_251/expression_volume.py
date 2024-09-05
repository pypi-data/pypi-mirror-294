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
from .expression_volume_child import expression_volume_child


class expression_volume(NamedObject[expression_volume_child], CreatableNamedObjectMixin[expression_volume_child]):
    """
    Provides access to creating new and editing existing expression-surfaces.
    """

    fluent_name = "expression-volume"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: expression_volume_child = expression_volume_child
    """
    child_object_type of expression_volume.
    """
