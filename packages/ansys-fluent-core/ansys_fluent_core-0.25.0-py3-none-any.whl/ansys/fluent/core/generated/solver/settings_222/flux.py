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

from .flux_child import flux_child


class flux(NamedObject[flux_child], CreatableNamedObjectMixinOld[flux_child]):
    """
    'flux' child.
    """

    fluent_name = "flux"

    child_object_type: flux_child = flux_child
    """
    child_object_type of flux.
    """
    return_type = "<object object at 0x7f57023d2570>"
