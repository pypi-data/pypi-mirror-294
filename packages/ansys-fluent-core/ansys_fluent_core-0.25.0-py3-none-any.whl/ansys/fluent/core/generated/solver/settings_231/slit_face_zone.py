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

from .zone_id import zone_id as zone_id_cls

class slit_face_zone(Command):
    """
    Slit a two-sided wall into two connected wall zones.
    
    Parameters
    ----------
        zone_id : int
            'zone_id' child.
    
    """

    fluent_name = "slit-face-zone"

    argument_names = \
        ['zone_id']

    _child_classes = dict(
        zone_id=zone_id_cls,
    )

    return_type = "<object object at 0x7f115b7b6960>"
