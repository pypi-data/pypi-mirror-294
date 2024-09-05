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

from .option_1 import option as option_cls
from .y_axis_direction import y_axis_direction as y_axis_direction_cls
from .y_axis_function_1 import y_axis_function as y_axis_function_cls

class y_axis_data(Group):
    """
    Options for Y axis function.
    """

    fluent_name = "y-axis-data"

    child_names = \
        ['option', 'y_axis_direction', 'y_axis_function']

    _child_classes = dict(
        option=option_cls,
        y_axis_direction=y_axis_direction_cls,
        y_axis_function=y_axis_function_cls,
    )

