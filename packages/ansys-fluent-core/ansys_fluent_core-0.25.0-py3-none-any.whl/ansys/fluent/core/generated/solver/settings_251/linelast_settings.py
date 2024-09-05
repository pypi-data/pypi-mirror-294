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

from .poisson_ratio import poisson_ratio as poisson_ratio_cls
from .amg_stabilization_1 import amg_stabilization as amg_stabilization_cls
from .max_iter_3 import max_iter as max_iter_cls
from .relative_tolerance_2 import relative_tolerance as relative_tolerance_cls
from .verbosity_10 import verbosity as verbosity_cls
from .smooth_from_ref import smooth_from_ref as smooth_from_ref_cls

class linelast_settings(Group):
    """
    'linelast_settings' child.
    """

    fluent_name = "linelast-settings"

    child_names = \
        ['poisson_ratio', 'amg_stabilization', 'max_iter',
         'relative_tolerance', 'verbosity', 'smooth_from_ref']

    _child_classes = dict(
        poisson_ratio=poisson_ratio_cls,
        amg_stabilization=amg_stabilization_cls,
        max_iter=max_iter_cls,
        relative_tolerance=relative_tolerance_cls,
        verbosity=verbosity_cls,
        smooth_from_ref=smooth_from_ref_cls,
    )

