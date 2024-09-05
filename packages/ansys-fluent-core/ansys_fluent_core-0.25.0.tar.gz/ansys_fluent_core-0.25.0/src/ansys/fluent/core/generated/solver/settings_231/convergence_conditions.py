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

from .convergence_reports import convergence_reports as convergence_reports_cls
from .frequency_1 import frequency as frequency_cls
from .condition import condition as condition_cls
from .check_for import check_for as check_for_cls

class convergence_conditions(Group):
    """
    'convergence_conditions' child.
    """

    fluent_name = "convergence-conditions"

    child_names = \
        ['convergence_reports', 'frequency', 'condition', 'check_for']

    _child_classes = dict(
        convergence_reports=convergence_reports_cls,
        frequency=frequency_cls,
        condition=condition_cls,
        check_for=check_for_cls,
    )

    return_type = "<object object at 0x7f115b6a9600>"
