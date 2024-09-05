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


class kernel_type(String, AllowedValuesMixin):
    """
    The basis function of the radial basis function, which has a strong effect on the speed of convergence, mesh quality, and smoothness of deformation.
    """

    fluent_name = "kernel-type"

