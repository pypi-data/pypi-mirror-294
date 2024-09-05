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

from .surface_tension import surface_tension as surface_tension_cls
from .surface_tension_model import surface_tension_model as surface_tension_model_cls
from .surface_tension_model_type import surface_tension_model_type as surface_tension_model_type_cls
from .wall_adhesion import wall_adhesion as wall_adhesion_cls

class forces(Group):
    """
    Specify interfacial forces.
    """

    fluent_name = "forces"

    child_names = \
        ['surface_tension', 'surface_tension_model',
         'surface_tension_model_type', 'wall_adhesion']

    _child_classes = dict(
        surface_tension=surface_tension_cls,
        surface_tension_model=surface_tension_model_cls,
        surface_tension_model_type=surface_tension_model_type_cls,
        wall_adhesion=wall_adhesion_cls,
    )

