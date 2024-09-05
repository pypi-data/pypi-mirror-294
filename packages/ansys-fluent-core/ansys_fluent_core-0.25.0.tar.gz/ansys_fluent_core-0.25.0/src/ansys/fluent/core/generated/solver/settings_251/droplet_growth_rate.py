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

from .option_3 import option as option_cls
from .young_alpha import young_alpha as young_alpha_cls
from .young_beta import young_beta as young_beta_cls

class droplet_growth_rate(Group):
    """
    Select the formula to model the droplet growth rate and set modeling parameters.
    """

    fluent_name = "droplet-growth-rate"

    child_names = \
        ['option', 'young_alpha', 'young_beta']

    _child_classes = dict(
        option=option_cls,
        young_alpha=young_alpha_cls,
        young_beta=young_beta_cls,
    )

