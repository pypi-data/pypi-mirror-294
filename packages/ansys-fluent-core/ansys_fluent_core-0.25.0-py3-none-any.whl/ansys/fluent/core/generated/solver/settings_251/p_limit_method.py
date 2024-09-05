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


class p_limit_method(String, AllowedValuesMixin):
    """
    It provides the pressure limit during properties calculation when pressure goes below the vapor pressure.
    """

    fluent_name = "p-limit-method"

