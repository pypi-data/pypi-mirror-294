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
from .center import center as center_cls
from .radius import radius as radius_cls
from .display_3 import display as display_cls

class sphere_slice_child(Group):
    """
    'child_object_type' of sphere_slice.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'center', 'radius']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        center=center_cls,
        radius=radius_cls,
        display=display_cls,
    )

    return_type = "<object object at 0x7f5cfb9b6690>"
