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

from .enabled_36 import enabled as enabled_cls
from .num_init_iter import num_init_iter as num_init_iter_cls

class predefined_workflow(Group):
    """
    Use predefined workflow.
    """

    fluent_name = "predefined-workflow"

    child_names = \
        ['enabled', 'num_init_iter']

    _child_classes = dict(
        enabled=enabled_cls,
        num_init_iter=num_init_iter_cls,
    )

