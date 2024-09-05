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

from .name import name as name_cls
from .phase_11 import phase as phase_cls

class network_child(Group):
    """
    'child_object_type' of network.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
    )

    return_type = "<object object at 0x7f5d094b5dc0>"
