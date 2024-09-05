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

from .name_13 import name as name_cls
from .surfaces_7 import surfaces as surfaces_cls

class group_surface_child(Group):
    """
    'child_object_type' of group_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'surfaces']

    _child_classes = dict(
        name=name_cls,
        surfaces=surfaces_cls,
    )

