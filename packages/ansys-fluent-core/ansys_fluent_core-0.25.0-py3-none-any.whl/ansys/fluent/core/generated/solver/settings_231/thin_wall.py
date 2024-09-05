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

from .shell_conduction_child import shell_conduction_child


class thin_wall(ListObject[shell_conduction_child]):
    """
    'thin_wall' child.
    """

    fluent_name = "thin-wall"

    child_object_type: shell_conduction_child = shell_conduction_child
    """
    child_object_type of thin_wall.
    """
    return_type = "<object object at 0x7f115ba12d40>"
