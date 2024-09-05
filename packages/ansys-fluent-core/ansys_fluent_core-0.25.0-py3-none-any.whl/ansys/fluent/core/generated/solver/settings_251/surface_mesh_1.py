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

from .surface_names_2 import surface_names as surface_names_cls

class surface_mesh(Command):
    """
    Draw the mesh defined by the specified surfaces.
    
    Parameters
    ----------
        surface_names : List
            Select surface.
    
    """

    fluent_name = "surface-mesh"

    argument_names = \
        ['surface_names']

    _child_classes = dict(
        surface_names=surface_names_cls,
    )

