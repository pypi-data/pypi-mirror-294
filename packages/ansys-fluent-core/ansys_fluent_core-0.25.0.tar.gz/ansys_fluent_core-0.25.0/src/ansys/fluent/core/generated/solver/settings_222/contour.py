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
from .contour_child import contour_child


class contour(NamedObject[contour_child], CreatableNamedObjectMixinOld[contour_child]):
    """
    'contour' child.
    """

    fluent_name = "contour"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: contour_child = contour_child
    """
    child_object_type of contour.
    """
    return_type = "<object object at 0x7f57023d3460>"
