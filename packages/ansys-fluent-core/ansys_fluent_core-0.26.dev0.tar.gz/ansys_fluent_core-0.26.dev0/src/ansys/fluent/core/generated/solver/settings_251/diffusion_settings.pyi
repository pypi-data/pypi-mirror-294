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

from .diffusion_coeff_function import diffusion_coeff_function as diffusion_coeff_function_cls
from .diffusion_coeff_parameter import diffusion_coeff_parameter as diffusion_coeff_parameter_cls
from .amg_stabilization_1 import amg_stabilization as amg_stabilization_cls
from .max_iter_2 import max_iter as max_iter_cls
from .relative_tolerance_1 import relative_tolerance as relative_tolerance_cls
from .verbosity_9 import verbosity as verbosity_cls
from .boundary_distance_method import boundary_distance_method as boundary_distance_method_cls
from .smooth_from_ref import smooth_from_ref as smooth_from_ref_cls
from .diffusion_fvm import diffusion_fvm as diffusion_fvm_cls

class diffusion_settings(Group):
    fluent_name = ...
    child_names = ...
    diffusion_coeff_function: diffusion_coeff_function_cls = ...
    diffusion_coeff_parameter: diffusion_coeff_parameter_cls = ...
    amg_stabilization: amg_stabilization_cls = ...
    max_iter: max_iter_cls = ...
    relative_tolerance: relative_tolerance_cls = ...
    verbosity: verbosity_cls = ...
    boundary_distance_method: boundary_distance_method_cls = ...
    smooth_from_ref: smooth_from_ref_cls = ...
    diffusion_fvm: diffusion_fvm_cls = ...
