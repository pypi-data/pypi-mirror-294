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

class mrf_to_sliding_mesh(Command):
    """
    Change motion specification from MRF to moving mesh.
    
    Parameters
    ----------
        zone_id : int
            'zone_id' child.
    
    """

    fluent_name = "mrf-to-sliding-mesh"

    argument_names = \
        ['zone_id']

    _child_classes = dict(
        zone_id=zone_id_cls,
    )

    return_type = "<object object at 0x7f115c1be850>"
