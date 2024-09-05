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

from .enabled_12 import enabled as enabled_cls

class ablation(Group):
    """
    Enable/disable ablation model.
    """

    fluent_name = "ablation"

    child_names = \
        ['enabled']

    _child_classes = dict(
        enabled=enabled_cls,
    )

    return_type = "<object object at 0x7f5ce12d6af0>"
