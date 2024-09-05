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

from .volume_child import volume_child


class volume(NamedObject[volume_child], CreatableNamedObjectMixinOld[volume_child]):
    """
    'volume' child.
    """

    fluent_name = "volume"

    child_object_type: volume_child = volume_child
    """
    child_object_type of volume.
    """
    return_type = "<object object at 0x7f57023d2090>"
