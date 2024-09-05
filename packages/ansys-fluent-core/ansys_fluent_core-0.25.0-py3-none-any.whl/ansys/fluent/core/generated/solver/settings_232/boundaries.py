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
from .boundaries_child import boundaries_child


class boundaries(NamedObject[boundaries_child], CreatableNamedObjectMixinOld[boundaries_child]):
    """
    'boundaries' child.
    """

    fluent_name = "boundaries"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: boundaries_child = boundaries_child
    """
    child_object_type of boundaries.
    """
    return_type = "<object object at 0x7f641d76a890>"
