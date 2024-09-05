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
from .ncopies import ncopies as ncopies_cls
from .offset_1 import offset as offset_cls
from .origin import origin as origin_cls
from .axis_1 import axis as axis_cls
from .angle import angle as angle_cls

class copy_cell_zones_by_delta(Command):
    """
    Copy cell zones by specifying an incremental translational or rotational offset.
    
    Parameters
    ----------
        cell_zones : List
            Specify names or IDs of cell zones to be copied. If an empty list is given, all active cell zones will be copied.
        translate : bool
            Specify whether the copying is translational or rotational.
        ncopies : int
            Specify how many copies to make.
        offset : List
            Specify the components of the incremental offset vector for translational copying.
        origin : List
            Specify the components of the origin vector for rotational copying.
        axis : List
            Specify the components of the axis vector for rotational copying.
        angle : real
            Specify the incremental angular offset for rotational copying.
    
    """

    fluent_name = "copy-cell-zones-by-delta"

    argument_names = \
        ['cell_zones', 'translate', 'ncopies', 'offset', 'origin', 'axis',
         'angle']

    _child_classes = dict(
        cell_zones=cell_zones_cls,
        translate=translate_cls,
        ncopies=ncopies_cls,
        offset=offset_cls,
        origin=origin_cls,
        axis=axis_cls,
        angle=angle_cls,
    )

