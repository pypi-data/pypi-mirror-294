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

from .wall_distance_free import wall_distance_free as wall_distance_free_cls
from .version import version as version_cls
from .cmix import cmix as cmix_cls
from .cjet import cjet as cjet_cls
from .blending_function import blending_function as blending_function_cls
from .auxiliary_constants import auxiliary_constants as auxiliary_constants_cls
from .geko_defaults import geko_defaults as geko_defaults_cls

class geko_options(Group):
    fluent_name = ...
    child_names = ...
    wall_distance_free: wall_distance_free_cls = ...
    version: version_cls = ...
    cmix: cmix_cls = ...
    cjet: cjet_cls = ...
    blending_function: blending_function_cls = ...
    auxiliary_constants: auxiliary_constants_cls = ...
    command_names = ...

    def geko_defaults(self, ):
        """
        Set GEKO options to default.
        """

