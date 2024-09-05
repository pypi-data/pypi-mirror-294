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

from .list_properties import list_properties as list_properties_cls
from .settings_child import settings_child


class settings(ListObject[settings_child]):
    """
    'settings' child.
    """

    fluent_name = "settings"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: settings_child = settings_child
    """
    child_object_type of settings.
    """
    return_type = "<object object at 0x7f5cfb8b5d10>"
