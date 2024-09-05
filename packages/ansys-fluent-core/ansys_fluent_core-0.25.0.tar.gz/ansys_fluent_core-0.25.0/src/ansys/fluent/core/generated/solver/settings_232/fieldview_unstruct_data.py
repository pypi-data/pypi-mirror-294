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

from .name import name as name_cls
from .surfaces_1 import surfaces as surfaces_cls
from .cellzones_1 import cellzones as cellzones_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls

class fieldview_unstruct_data(Command):
    """
    Write a Fieldview unstructured results only file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surfaces : List
            List of surfaces to export.
        cellzones : List
            List of cell zones to export.
        cell_func_domain : List
            'cell_func_domain' child.
    
    """

    fluent_name = "fieldview-unstruct-data"

    argument_names = \
        ['name', 'surfaces', 'cellzones', 'cell_func_domain']

    _child_classes = dict(
        name=name_cls,
        surfaces=surfaces_cls,
        cellzones=cellzones_cls,
        cell_func_domain=cell_func_domain_cls,
    )

    return_type = "<object object at 0x7f641facfc00>"
