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
from .surface_3 import surface as surface_cls
from .zones_5 import zones as zones_cls
from .volumes_1 import volumes as volumes_cls
from .display_4 import display as display_cls

class imprint_surface_child(Group):
    """
    'child_object_type' of imprint_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'surface', 'zones', 'volumes']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        surface=surface_cls,
        zones=zones_cls,
        volumes=volumes_cls,
        display=display_cls,
    )

