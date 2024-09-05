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

from .track_zone import track_zone as track_zone_cls

class zone_track(Group):
    """
    'zone_track' child.
    """

    fluent_name = "zone-track"

    child_names = \
        ['track_zone']

    _child_classes = dict(
        track_zone=track_zone_cls,
    )

    return_type = "<object object at 0x7f641d76ab90>"
