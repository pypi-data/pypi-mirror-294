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

from .x import x as x_cls
from .y import y as y_cls
from .z import z as z_cls

class r(Group):
    """
    'r' child.
    """

    fluent_name = "r"

    child_names = \
        ['x', 'y', 'z']

    _child_classes = dict(
        x=x_cls,
        y=y_cls,
        z=z_cls,
    )

    return_type = "<object object at 0x7f115d64ec20>"
