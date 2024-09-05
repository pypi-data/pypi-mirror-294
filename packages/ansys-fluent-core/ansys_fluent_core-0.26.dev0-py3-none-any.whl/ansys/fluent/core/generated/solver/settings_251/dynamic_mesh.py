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

from .enabled_38 import enabled as enabled_cls
from .methods import methods as methods_cls

class dynamic_mesh(Group):
    """
    'dynamic_mesh' child.
    """

    fluent_name = "dynamic-mesh"

    child_names = \
        ['enabled', 'methods']

    _child_classes = dict(
        enabled=enabled_cls,
        methods=methods_cls,
    )

