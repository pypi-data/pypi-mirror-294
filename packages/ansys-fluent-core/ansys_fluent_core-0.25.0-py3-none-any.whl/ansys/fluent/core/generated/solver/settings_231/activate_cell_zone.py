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

from .cell_zone_list import cell_zone_list as cell_zone_list_cls

class activate_cell_zone(Command):
    """
    'activate_cell_zone' command.
    
    Parameters
    ----------
        cell_zone_list : List
            'cell_zone_list' child.
    
    """

    fluent_name = "activate-cell-zone"

    argument_names = \
        ['cell_zone_list']

    _child_classes = dict(
        cell_zone_list=cell_zone_list_cls,
    )

    return_type = "<object object at 0x7f115c1be820>"
