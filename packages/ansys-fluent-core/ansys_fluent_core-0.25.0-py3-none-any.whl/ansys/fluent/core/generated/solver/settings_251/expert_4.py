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

from .backward_compatibility import backward_compatibility as backward_compatibility_cls
from .flux_scaling import flux_scaling as flux_scaling_cls
from .nps_minimize_po_loss import nps_minimize_po_loss as nps_minimize_po_loss_cls
from .print_settings import print_settings as print_settings_cls
from .get_po_loss_settings import get_po_loss_settings as get_po_loss_settings_cls
from .get_flux_settings import get_flux_settings as get_flux_settings_cls

class expert(Group):
    """
    Configure expert parameters for turbo interfaces.
    """

    fluent_name = "expert"

    child_names = \
        ['backward_compatibility']

    command_names = \
        ['flux_scaling', 'nps_minimize_po_loss', 'print_settings']

    query_names = \
        ['get_po_loss_settings', 'get_flux_settings']

    _child_classes = dict(
        backward_compatibility=backward_compatibility_cls,
        flux_scaling=flux_scaling_cls,
        nps_minimize_po_loss=nps_minimize_po_loss_cls,
        print_settings=print_settings_cls,
        get_po_loss_settings=get_po_loss_settings_cls,
        get_flux_settings=get_flux_settings_cls,
    )

