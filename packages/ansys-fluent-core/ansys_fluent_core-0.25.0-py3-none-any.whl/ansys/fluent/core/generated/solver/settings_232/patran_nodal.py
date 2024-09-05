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
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class patran_nodal(Command):
    """
    Write a PATRAN nodal results file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surfaces : List
            'surfaces' child.
        cell_func_domain_export : List
            'cell_func_domain_export' child.
    
    """

    fluent_name = "patran-nodal"

    argument_names = \
        ['name', 'surfaces', 'cell_func_domain_export']

    _child_classes = dict(
        name=name_cls,
        surfaces=surfaces_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

    return_type = "<object object at 0x7f641facf980>"
