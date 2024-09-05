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

from .beach_dir_list_child import beach_dir_list_child


class beach_dir_list(ListObject[beach_dir_list_child]):
    """
    'beach_dir_list' child.
    """

    fluent_name = "beach-dir-list"

    child_object_type: beach_dir_list_child = beach_dir_list_child
    """
    child_object_type of beach_dir_list.
    """
    return_type = "<object object at 0x7f115c39eb60>"
