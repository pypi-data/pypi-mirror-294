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

from .option import option as option_cls
from .file_name_1 import file_name as file_name_cls
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls

class fieldview_unstruct_surfaces(Command):
    """
    Write a Fieldview unstructured surface mesh, data.
    
    Parameters
    ----------
        option : str
            'option' child.
        file_name : str
            'file_name' child.
        surfaces : List
            Select surface.
        cell_func_domain : List
            'cell_func_domain' child.
    
    """

    fluent_name = "fieldview-unstruct-surfaces"

    argument_names = \
        ['option', 'file_name', 'surfaces', 'cell_func_domain']

    _child_classes = dict(
        option=option_cls,
        file_name=file_name_cls,
        surfaces=surfaces_cls,
        cell_func_domain=cell_func_domain_cls,
    )

    return_type = "<object object at 0x7f5d0a063cf0>"
