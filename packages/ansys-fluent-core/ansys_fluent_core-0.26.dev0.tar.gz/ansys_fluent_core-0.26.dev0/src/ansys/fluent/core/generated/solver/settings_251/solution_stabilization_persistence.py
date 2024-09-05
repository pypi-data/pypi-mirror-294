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


class solution_stabilization_persistence(String, AllowedValuesMixin):
    """
    Persistence of the solution stabilization based on events [0-contact based, 1-always on].
    """

    fluent_name = "solution-stabilization-persistence"

