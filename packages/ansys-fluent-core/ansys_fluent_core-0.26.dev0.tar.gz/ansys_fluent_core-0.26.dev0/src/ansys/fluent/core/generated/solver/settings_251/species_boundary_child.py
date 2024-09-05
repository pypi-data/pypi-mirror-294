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

from .fuel import fuel as fuel_cls
from .oxidizer import oxidizer as oxidizer_cls

class species_boundary_child(Group):
    """
    'child_object_type' of species_boundary.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['fuel', 'oxidizer']

    _child_classes = dict(
        fuel=fuel_cls,
        oxidizer=oxidizer_cls,
    )

