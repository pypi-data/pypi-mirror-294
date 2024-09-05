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

from .linearize import linearize as linearize_cls
from .threshold import threshold as threshold_cls

class continuity_transient_term_linearization(Group):
    """
    Enter continuity transient term linearization.
    """

    fluent_name = "continuity-transient-term-linearization"

    child_names = \
        ['linearize', 'threshold']

    _child_classes = dict(
        linearize=linearize_cls,
        threshold=threshold_cls,
    )

