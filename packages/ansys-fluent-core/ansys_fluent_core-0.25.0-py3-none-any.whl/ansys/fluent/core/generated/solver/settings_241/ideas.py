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
from .surfaces_1 import surfaces as surfaces_cls
from .structural_analysis import structural_analysis as structural_analysis_cls
from .write_loads import write_loads as write_loads_cls
from .loads import loads as loads_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class ideas(Command):
    """
    Write an IDEAS universal file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surfaces : List
            List of surfaces to export.
        structural_analysis : bool
            'structural_analysis' child.
        write_loads : bool
            'write_loads' child.
        loads : List
            'loads' child.
        cell_func_domain_export : List
            'cell_func_domain_export' child.
    
    """

    fluent_name = "ideas"

    argument_names = \
        ['file_name', 'surfaces', 'structural_analysis', 'write_loads',
         'loads', 'cell_func_domain_export']

    _child_classes = dict(
        file_name=file_name_cls,
        surfaces=surfaces_cls,
        structural_analysis=structural_analysis_cls,
        write_loads=write_loads_cls,
        loads=loads_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

    return_type = "<object object at 0x7f5d0a063c70>"
