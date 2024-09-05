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

from .initial_fourier_number import initial_fourier_number as initial_fourier_number_cls
from .fourier_number_multiplier import fourier_number_multiplier as fourier_number_multiplier_cls
from .relative_tolerance import relative_tolerance as relative_tolerance_cls
from .absolute_tolerance import absolute_tolerance as absolute_tolerance_cls
from .flamelet_convergence_tolerance import flamelet_convergence_tolerance as flamelet_convergence_tolerance_cls
from .maximum_integration_time import maximum_integration_time as maximum_integration_time_cls

class control(Group):
    """
    PDF Control Options.
    """

    fluent_name = "control"

    child_names = \
        ['initial_fourier_number', 'fourier_number_multiplier',
         'relative_tolerance', 'absolute_tolerance',
         'flamelet_convergence_tolerance', 'maximum_integration_time']

    _child_classes = dict(
        initial_fourier_number=initial_fourier_number_cls,
        fourier_number_multiplier=fourier_number_multiplier_cls,
        relative_tolerance=relative_tolerance_cls,
        absolute_tolerance=absolute_tolerance_cls,
        flamelet_convergence_tolerance=flamelet_convergence_tolerance_cls,
        maximum_integration_time=maximum_integration_time_cls,
    )

