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

from .domain_2 import domain as domain_cls
from .zones_9 import zones as zones_cls
from .physics_2 import physics as physics_cls

class get_pressure_work(Query):
    """
    Print pressure work rate at moving boundaries.
    
    Parameters
    ----------
        domain : str
            Select the domain.
        zones : List
            Select zone name.
        physics : List
            Select the physics location.
    
    """

    fluent_name = "get-pressure-work"

    argument_names = \
        ['domain', 'zones', 'physics']

    _child_classes = dict(
        domain=domain_cls,
        zones=zones_cls,
        physics=physics_cls,
    )

