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

from .stoichiometric_mixture_fraction_1 import stoichiometric_mixture_fraction as stoichiometric_mixture_fraction_cls
from .user_mixture_fraction import user_mixture_fraction as user_mixture_fraction_cls
from .user_mixture_fraction_value import user_mixture_fraction_value as user_mixture_fraction_value_cls

class refine_based(Group):
    """
    Auto Refine Flamelet in Mixture Fraction Options.
    """

    fluent_name = "refine-based"

    child_names = \
        ['stoichiometric_mixture_fraction', 'user_mixture_fraction',
         'user_mixture_fraction_value']

    _child_classes = dict(
        stoichiometric_mixture_fraction=stoichiometric_mixture_fraction_cls,
        user_mixture_fraction=user_mixture_fraction_cls,
        user_mixture_fraction_value=user_mixture_fraction_value_cls,
    )

