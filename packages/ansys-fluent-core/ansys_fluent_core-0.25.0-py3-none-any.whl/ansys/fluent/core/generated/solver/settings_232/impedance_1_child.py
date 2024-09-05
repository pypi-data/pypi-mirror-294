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

from .pole import pole as pole_cls
from .amplitude import amplitude as amplitude_cls

class impedance_1_child(Group):
    """
    'child_object_type' of impedance_1.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pole', 'amplitude']

    _child_classes = dict(
        pole=pole_cls,
        amplitude=amplitude_cls,
    )

    return_type = "<object object at 0x7f641eb8c970>"
