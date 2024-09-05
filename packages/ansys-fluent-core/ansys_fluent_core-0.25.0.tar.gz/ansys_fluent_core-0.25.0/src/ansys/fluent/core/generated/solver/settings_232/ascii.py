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
from .surface_name_list_1 import surface_name_list as surface_name_list_cls
from .delimiter import delimiter as delimiter_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls
from .location import location as location_cls

class ascii(Command):
    """
    Write an ASCII file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surface_name_list : List
            List of surfaces to export.
        delimiter : str
            'delimiter' child.
        cell_func_domain : List
            'cell_func_domain' child.
        location : str
            'location' child.
    
    """

    fluent_name = "ascii"

    argument_names = \
        ['name', 'surface_name_list', 'delimiter', 'cell_func_domain',
         'location']

    _child_classes = dict(
        name=name_cls,
        surface_name_list=surface_name_list_cls,
        delimiter=delimiter_cls,
        cell_func_domain=cell_func_domain_cls,
        location=location_cls,
    )

    return_type = "<object object at 0x7f641face900>"
