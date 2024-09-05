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

from .local_dt import local_dt as local_dt_cls
from .global_dt import global_dt as global_dt_cls

class advanced_options(Group):
    """
    'advanced_options' child.
    """

    fluent_name = "advanced-options"

    child_names = \
        ['local_dt', 'global_dt']

    _child_classes = dict(
        local_dt=local_dt_cls,
        global_dt=global_dt_cls,
    )

    return_type = "<object object at 0x7f57023d1e20>"
