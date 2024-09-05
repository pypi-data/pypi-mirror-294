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

from .surface_name import surface_name as surface_name_cls
from .type_14 import type as type_cls
from .inclusion import inclusion as inclusion_cls
from .input_coordinates import input_coordinates as input_coordinates_cls
from .surfaces_21 import surfaces as surfaces_cls

class create_region_clip_surface(Command):
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

    fluent_name = "create-region-clip-surface"

    argument_names = \
        ['surface_name', 'type', 'inclusion', 'input_coordinates', 'surfaces']

    _child_classes = dict(
        surface_name=surface_name_cls,
        type=type_cls,
        inclusion=inclusion_cls,
        input_coordinates=input_coordinates_cls,
        surfaces=surfaces_cls,
    )

