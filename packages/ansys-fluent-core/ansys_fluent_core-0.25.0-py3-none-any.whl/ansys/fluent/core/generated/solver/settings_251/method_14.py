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


class method(String, AllowedValuesMixin):
    """
    None: Solves adjoint equations with no stabilization.
    Dissipation: Introduces nonlinear damping in calculation domain.
    """

    fluent_name = "method"

