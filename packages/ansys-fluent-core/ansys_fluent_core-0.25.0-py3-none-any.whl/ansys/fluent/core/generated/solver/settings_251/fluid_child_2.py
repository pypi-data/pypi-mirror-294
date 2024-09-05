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

from .name_2 import name as name_cls
from .location_2 import location as location_cls
from .settings_4 import settings as settings_cls
from .boundaries import boundaries as boundaries_cls
from .split import split as split_cls

class fluid_child(Group):
    """
    'child_object_type' of fluid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'location', 'settings', 'boundaries']

    command_names = \
        ['split']

    _child_classes = dict(
        name=name_cls,
        location=location_cls,
        settings=settings_cls,
        boundaries=boundaries_cls,
        split=split_cls,
    )

