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
from .settings_17 import settings as settings_cls

class outlet_vent_child(Group):
    """
    'child_object_type' of outlet_vent.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'location', 'settings']

    _child_classes = dict(
        name=name_cls,
        location=location_cls,
        settings=settings_cls,
    )

