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

from .file_name_2 import file_name as file_name_cls
from .view_list import view_list as view_list_cls

class write_views(Command):
    """
    Write selected views to a view file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        view_list : List
            'view_list' child.
    
    """

    fluent_name = "write-views"

    argument_names = \
        ['file_name', 'view_list']

    _child_classes = dict(
        file_name=file_name_cls,
        view_list=view_list_cls,
    )

