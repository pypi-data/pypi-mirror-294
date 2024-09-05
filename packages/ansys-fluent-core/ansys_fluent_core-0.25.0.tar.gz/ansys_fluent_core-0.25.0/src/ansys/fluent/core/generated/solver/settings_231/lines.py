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

from .lines_child import lines_child


class lines(ListObject[lines_child]):
    """
    'lines' child.
    """

    fluent_name = "lines"

    child_object_type: lines_child = lines_child
    """
    child_object_type of lines.
    """
    return_type = "<object object at 0x7f115b5a06c0>"
