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


class stagnation_conditions(String, AllowedValuesMixin):
    """
    If the gas phase is selected, zero wetness is assumed when evaluating total or static values of pressure and temperature.
    """

    fluent_name = "stagnation-conditions"

