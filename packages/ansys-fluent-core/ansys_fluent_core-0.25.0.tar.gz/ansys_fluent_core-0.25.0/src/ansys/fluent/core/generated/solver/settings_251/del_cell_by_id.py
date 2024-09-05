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

from .cellids import cellids as cellids_cls
from .augment import augment as augment_cls

class del_cell_by_id(Command):
    """
    Delete cells based on cell ids.
    
    Parameters
    ----------
        cellids : List
            Provide a list of cell ids.
        augment : bool
            Augment list of cells to meet nunerics requirement.
    
    """

    fluent_name = "del-cell-by-id"

    argument_names = \
        ['cellids', 'augment']

    _child_classes = dict(
        cellids=cellids_cls,
        augment=augment_cls,
    )

