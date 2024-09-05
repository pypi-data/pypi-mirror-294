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

from .number_of_eulerian_phases import number_of_eulerian_phases as number_of_eulerian_phases_cls

class number_of_phases(Group):
    """
    Number of phases settings.
    """

    fluent_name = "number-of-phases"

    child_names = \
        ['number_of_eulerian_phases']

    _child_classes = dict(
        number_of_eulerian_phases=number_of_eulerian_phases_cls,
    )

