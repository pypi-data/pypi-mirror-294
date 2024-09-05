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

from typing import Union, List, Tuple

from .expert_9 import expert as expert_cls
from .interpolate_2 import interpolate as interpolate_cls
from .create_region_clip_surface import create_region_clip_surface as create_region_clip_surface_cls

class utilities(Group):
    fluent_name = ...
    child_names = ...
    expert: expert_cls = ...
    interpolate: interpolate_cls = ...
    command_names = ...

    def create_region_clip_surface(self, surface_name: str, type: str, inclusion: str, input_coordinates: List[Union[float, str]], surfaces: List[str]):
        """
        Create a surface by clipping other surfaces.
        
        Parameters
        ----------
            surface_name : str
                Name of the surface to be created.
            type : str
                Type of the surface to be created.
            inclusion : str
                Domain included inside or outside specified shape.
            input_coordinates : List
                Design variable minimum and maximum.
            surfaces : List
                Specify surfaces to clip.
        
        """

