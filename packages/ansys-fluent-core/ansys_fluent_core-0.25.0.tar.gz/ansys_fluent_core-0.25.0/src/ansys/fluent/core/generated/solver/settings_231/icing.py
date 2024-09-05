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

from .icing_child import icing_child


class icing(NamedObject[icing_child], CreatableNamedObjectMixinOld[icing_child]):
    """
    'icing' child.
    """

    fluent_name = "icing"

    child_object_type: icing_child = icing_child
    """
    child_object_type of icing.
    """
    return_type = "<object object at 0x7f115b6a9080>"
