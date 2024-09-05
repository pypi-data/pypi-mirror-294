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

from .cell_zones_5 import cell_zones as cell_zones_cls
from .translate_1 import translate as translate_cls
from .offsets import offsets as offsets_cls
from .origin import origin as origin_cls
from .axis_1 import axis as axis_cls
from .angles import angles as angles_cls

class copy_cell_zones_by_offsets(Command):
    """
    Copy cell zones by specifying absolute translational or rotational offsets.
    
    Parameters
    ----------
        cell_zones : List
            Specify names or IDs of cell zones to be copied. If an empty list is given, all active cell zones will be copied.
        translate : bool
            Specify whether the copying is translational or rotational.
        offsets : List
            Specify the components of each offset vector for translational copying.
        origin : List
            Specify the components of the origin vector for rotational copying.
        axis : List
            Specify the components of the axis vector for rotational copying.
        angles : List
            Specify the angular offsets for rotational copying.
    
    """

    fluent_name = "copy-cell-zones-by-offsets"

    argument_names = \
        ['cell_zones', 'translate', 'offsets', 'origin', 'axis', 'angles']

    _child_classes = dict(
        cell_zones=cell_zones_cls,
        translate=translate_cls,
        offsets=offsets_cls,
        origin=origin_cls,
        axis=axis_cls,
        angles=angles_cls,
    )

