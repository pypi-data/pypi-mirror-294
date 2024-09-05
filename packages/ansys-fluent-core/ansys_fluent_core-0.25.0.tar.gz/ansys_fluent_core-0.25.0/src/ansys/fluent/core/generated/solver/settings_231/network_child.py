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

from .phase_10 import phase as phase_cls

class network_child(Group):
    """
    'child_object_type' of network.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase']

    _child_classes = dict(
        phase=phase_cls,
    )

    return_type = "<object object at 0x7f115cce6d20>"
