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

from .variance_method import variance_method as variance_method_cls
from .algebraic_variance_constant import algebraic_variance_constant as algebraic_variance_constant_cls

class variance_settings(Group):
    """
    Specify Variance Settings.
    """

    fluent_name = "variance-settings"

    child_names = \
        ['variance_method', 'algebraic_variance_constant']

    _child_classes = dict(
        variance_method=variance_method_cls,
        algebraic_variance_constant=algebraic_variance_constant_cls,
    )

