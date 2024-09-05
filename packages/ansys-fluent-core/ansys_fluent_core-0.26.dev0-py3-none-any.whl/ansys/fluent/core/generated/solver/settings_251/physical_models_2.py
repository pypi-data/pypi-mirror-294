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

from .use_multi_physics import use_multi_physics as use_multi_physics_cls
from .threshold_1 import threshold as threshold_cls
from .interval import interval as interval_cls

class physical_models(Group):
    """
    Use physical-models load balancing?.
    """

    fluent_name = "physical-models"

    child_names = \
        ['use_multi_physics', 'threshold', 'interval']

    _child_classes = dict(
        use_multi_physics=use_multi_physics_cls,
        threshold=threshold_cls,
        interval=interval_cls,
    )

