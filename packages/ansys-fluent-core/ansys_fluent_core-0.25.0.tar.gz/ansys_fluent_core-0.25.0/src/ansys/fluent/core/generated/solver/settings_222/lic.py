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

from .display import display as display_cls
from .lic_child import lic_child


class lic(NamedObject[lic_child], CreatableNamedObjectMixinOld[lic_child]):
    """
    'lic' child.
    """

    fluent_name = "lic"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: lic_child = lic_child
    """
    child_object_type of lic.
    """
    return_type = "<object object at 0x7f57022dc8e0>"
