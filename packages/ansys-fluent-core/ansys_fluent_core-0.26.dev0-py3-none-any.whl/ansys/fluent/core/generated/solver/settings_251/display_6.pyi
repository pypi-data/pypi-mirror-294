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

from .surface_mesh_1 import surface_mesh as surface_mesh_cls
from .zone_mesh import zone_mesh as zone_mesh_cls

class display(Group):
    fluent_name = ...
    command_names = ...

    def surface_mesh(self, surface_names: List[str]):
        """
        Draw the mesh defined by the specified surfaces.
        
        Parameters
        ----------
            surface_names : List
                Select surface.
        
        """

    def zone_mesh(self, zone_names: List[str]):
        """
        Draw the mesh defined by specified face zones.
        
        Parameters
        ----------
            zone_names : List
                Enter zone name list.
        
        """

