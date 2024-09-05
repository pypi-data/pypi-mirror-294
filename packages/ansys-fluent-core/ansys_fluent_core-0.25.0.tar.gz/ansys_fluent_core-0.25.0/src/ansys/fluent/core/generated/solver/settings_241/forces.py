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

from .option import option as option_cls
from .domain import domain as domain_cls
from .all_wall_zones import all_wall_zones as all_wall_zones_cls
from .wall_zones_1 import wall_zones as wall_zones_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .momentum_center import momentum_center as momentum_center_cls
from .momentum_axis import momentum_axis as momentum_axis_cls
from .pressure_coordinate import pressure_coordinate as pressure_coordinate_cls
from .coordinate_value import coordinate_value as coordinate_value_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class forces(Command):
    """
    'forces' command.
    
    Parameters
    ----------
        option : str
            'option' child.
        domain : str
            'domain' child.
        all_wall_zones : bool
            Select all wall zones available.
        wall_zones : List
            Enter wall zone name list.
        direction_vector : List
            'direction_vector' child.
        momentum_center : List
            'momentum_center' child.
        momentum_axis : List
            'momentum_axis' child.
        pressure_coordinate : str
            'pressure_coordinate' child.
        coordinate_value : real
            'coordinate_value' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
    
    """

    fluent_name = "forces"

    argument_names = \
        ['option', 'domain', 'all_wall_zones', 'wall_zones',
         'direction_vector', 'momentum_center', 'momentum_axis',
         'pressure_coordinate', 'coordinate_value', 'write_to_file',
         'file_name', 'append_data']

    _child_classes = dict(
        option=option_cls,
        domain=domain_cls,
        all_wall_zones=all_wall_zones_cls,
        wall_zones=wall_zones_cls,
        direction_vector=direction_vector_cls,
        momentum_center=momentum_center_cls,
        momentum_axis=momentum_axis_cls,
        pressure_coordinate=pressure_coordinate_cls,
        coordinate_value=coordinate_value_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

    return_type = "<object object at 0x7f5cfb7b3840>"
