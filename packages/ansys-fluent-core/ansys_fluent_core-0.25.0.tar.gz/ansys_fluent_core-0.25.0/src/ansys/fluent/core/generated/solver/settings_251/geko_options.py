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

from .wall_distance_free import wall_distance_free as wall_distance_free_cls
from .version import version as version_cls
from .cmix import cmix as cmix_cls
from .cjet import cjet as cjet_cls
from .blending_function import blending_function as blending_function_cls
from .auxiliary_constants import auxiliary_constants as auxiliary_constants_cls
from .geko_defaults import geko_defaults as geko_defaults_cls

class geko_options(Group):
    """
    'geko_options' child.
    """

    fluent_name = "geko-options"

    child_names = \
        ['wall_distance_free', 'version', 'cmix', 'cjet', 'blending_function',
         'auxiliary_constants']

    command_names = \
        ['geko_defaults']

    _child_classes = dict(
        wall_distance_free=wall_distance_free_cls,
        version=version_cls,
        cmix=cmix_cls,
        cjet=cjet_cls,
        blending_function=blending_function_cls,
        auxiliary_constants=auxiliary_constants_cls,
        geko_defaults=geko_defaults_cls,
    )

    _child_aliases = dict(
        cbf_lam="auxiliary_constants/cbf_lam",
        cbf_tur="auxiliary_constants/cbf_tur",
        cjet_aux="auxiliary_constants/cjet_aux",
        cnw_sub="auxiliary_constants/cnw_sub",
        creal="auxiliary_constants/creal",
    )

