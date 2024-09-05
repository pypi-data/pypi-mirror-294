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

from .enabled_1 import enabled as enabled_cls

class ablation(Group):
    """
    'ablation' child.
    """

    fluent_name = "ablation"

    child_names = \
        ['enabled']

    _child_classes = dict(
        enabled=enabled_cls,
    )

    return_type = "<object object at 0x7f63fefe2150>"
