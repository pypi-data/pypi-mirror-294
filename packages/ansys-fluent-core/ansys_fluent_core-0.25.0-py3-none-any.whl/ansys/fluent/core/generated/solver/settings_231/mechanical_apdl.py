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
from .thread_name_list import thread_name_list as thread_name_list_cls

class mechanical_apdl(Command):
    """
    Write an Mechanical APDL file.
    
    Parameters
    ----------
        name : str
            'name' child.
        thread_name_list : List
            'thread_name_list' child.
    
    """

    fluent_name = "mechanical-apdl"

    argument_names = \
        ['name', 'thread_name_list']

    _child_classes = dict(
        name=name_cls,
        thread_name_list=thread_name_list_cls,
    )

    return_type = "<object object at 0x7f115d64e670>"
