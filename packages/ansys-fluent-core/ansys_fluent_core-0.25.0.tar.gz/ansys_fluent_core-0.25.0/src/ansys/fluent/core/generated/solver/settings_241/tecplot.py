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

from .file_name_1 import file_name as file_name_cls
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class tecplot(Command):
    """
    Write a Tecplot+3DV format file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surfaces : List
            Select surface.
        cell_func_domain_export : List
            'cell_func_domain_export' child.
    
    """

    fluent_name = "tecplot"

    argument_names = \
        ['file_name', 'surfaces', 'cell_func_domain_export']

    _child_classes = dict(
        file_name=file_name_cls,
        surfaces=surfaces_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

    return_type = "<object object at 0x7f5d0a063ab0>"
