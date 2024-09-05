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

from .pre_sweeps_3 import pre_sweeps as pre_sweeps_cls
from .post_sweeps_2 import post_sweeps as post_sweeps_cls

class fixed_cycle_parameters(Group):
    """
    'fixed_cycle_parameters' child.
    """

    fluent_name = "fixed-cycle-parameters"

    child_names = \
        ['pre_sweeps', 'post_sweeps']

    _child_classes = dict(
        pre_sweeps=pre_sweeps_cls,
        post_sweeps=post_sweeps_cls,
    )

    return_type = "<object object at 0x7f641d660a00>"
