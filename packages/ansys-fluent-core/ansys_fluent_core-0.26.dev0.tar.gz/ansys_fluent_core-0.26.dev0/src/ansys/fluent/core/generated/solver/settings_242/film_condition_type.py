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


class film_condition_type(String, AllowedValuesMixin):
    """
    Film Condition Type (0: Boundary Condition, 1: Initial Condition).
    """

    fluent_name = "film-condition-type"

