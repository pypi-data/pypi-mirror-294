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

from .name_11 import name as name_cls
from .options_20 import options as options_cls
from .y_axis_function import y_axis_function as y_axis_function_cls
from .x_axis_function_1 import x_axis_function as x_axis_function_cls
from .x_axis_data import x_axis_data as x_axis_data_cls
from .y_axis_data import y_axis_data as y_axis_data_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .option_38 import option as option_cls
from .plot_direction import plot_direction as plot_direction_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .surfaces_4 import surfaces as surfaces_cls
from .axes_1 import axes as axes_cls
from .curves_1 import curves as curves_cls
from .display_7 import display as display_cls
from .write_to_file import write_to_file as write_to_file_cls
from .read_from_file import read_from_file as read_from_file_cls
from .free_file_data import free_file_data as free_file_data_cls

class xy_plot_child(Group):
    """
    'child_object_type' of xy_plot.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'options', 'y_axis_function', 'x_axis_function',
         'x_axis_data', 'y_axis_data', 'surfaces_list', 'option',
         'plot_direction', 'physics', 'geometry', 'surfaces', 'axes',
         'curves']

    command_names = \
        ['display', 'write_to_file', 'read_from_file', 'free_file_data']

    _child_classes = dict(
        name=name_cls,
        options=options_cls,
        y_axis_function=y_axis_function_cls,
        x_axis_function=x_axis_function_cls,
        x_axis_data=x_axis_data_cls,
        y_axis_data=y_axis_data_cls,
        surfaces_list=surfaces_list_cls,
        option=option_cls,
        plot_direction=plot_direction_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        surfaces=surfaces_cls,
        axes=axes_cls,
        curves=curves_cls,
        display=display_cls,
        write_to_file=write_to_file_cls,
        read_from_file=read_from_file_cls,
        free_file_data=free_file_data_cls,
    )

