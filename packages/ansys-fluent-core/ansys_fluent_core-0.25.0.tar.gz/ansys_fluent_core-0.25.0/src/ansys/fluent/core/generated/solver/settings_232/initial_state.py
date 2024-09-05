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

from .origin import origin as origin_cls
from .orientation import orientation as orientation_cls

class initial_state(Group):
    """
    'initial_state' child.
    """

    fluent_name = "initial-state"

    child_names = \
        ['origin', 'orientation']

    _child_classes = dict(
        origin=origin_cls,
        orientation=orientation_cls,
    )

    return_type = "<object object at 0x7f641d76ae00>"
