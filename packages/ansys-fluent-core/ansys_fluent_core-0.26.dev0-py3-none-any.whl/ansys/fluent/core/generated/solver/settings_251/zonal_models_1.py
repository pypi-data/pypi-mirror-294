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

from .zonal_models import zonal_models as zonal_models_cls
from .zonal_flow import zonal_flow as zonal_flow_cls
from .zonal_flow_spec import zonal_flow_spec as zonal_flow_spec_cls
from .zonal_pseudo_time_spec import zonal_pseudo_time_spec as zonal_pseudo_time_spec_cls

class zonal_models(Group):
    """
    Zonal flow model settings.
    """

    fluent_name = "zonal-models"

    child_names = \
        ['zonal_models', 'zonal_flow', 'zonal_flow_spec',
         'zonal_pseudo_time_spec']

    _child_classes = dict(
        zonal_models=zonal_models_cls,
        zonal_flow=zonal_flow_cls,
        zonal_flow_spec=zonal_flow_spec_cls,
        zonal_pseudo_time_spec=zonal_pseudo_time_spec_cls,
    )

