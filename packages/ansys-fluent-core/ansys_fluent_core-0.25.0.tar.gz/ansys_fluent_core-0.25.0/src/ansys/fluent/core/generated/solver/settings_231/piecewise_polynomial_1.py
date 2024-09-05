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

from .piecewise_polynomial_child_1 import piecewise_polynomial_child


class piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    """
    'piecewise_polynomial' child.
    """

    fluent_name = "piecewise-polynomial"

    child_object_type: piecewise_polynomial_child = piecewise_polynomial_child
    """
    child_object_type of piecewise_polynomial.
    """
    return_type = "<object object at 0x7f115c39e470>"
