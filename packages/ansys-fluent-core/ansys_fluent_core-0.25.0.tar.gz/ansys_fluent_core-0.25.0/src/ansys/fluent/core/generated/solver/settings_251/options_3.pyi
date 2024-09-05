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

from typing import Union, List, Tuple

from .inlet_diffusion_2 import inlet_diffusion as inlet_diffusion_cls
from .compressibility import compressibility as compressibility_cls
from .liquid_micro_mix import liquid_micro_mix as liquid_micro_mix_cls
from .stoichiometric_mixture_fraction import stoichiometric_mixture_fraction as stoichiometric_mixture_fraction_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    inlet_diffusion: inlet_diffusion_cls = ...
    compressibility: compressibility_cls = ...
    liquid_micro_mix: liquid_micro_mix_cls = ...
    stoichiometric_mixture_fraction: stoichiometric_mixture_fraction_cls = ...
