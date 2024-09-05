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

from .change_type import change_type as change_type_cls
from .interior_child import interior_child


class interior(NamedObject[interior_child], CreatableNamedObjectMixinOld[interior_child]):
    """
    'interior' child.
    """

    fluent_name = "interior"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: interior_child = interior_child
    """
    child_object_type of interior.
    """
    return_type = "<object object at 0x7f57030d35f0>"
