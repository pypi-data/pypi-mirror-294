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

from .command_list import command_list as command_list_cls
from .filename import filename as filename_cls

class export_modifications(Command):
    """
    Export all case modifications to a tsv file.
    
    Parameters
    ----------
        command_list : List
            'command_list' child.
        filename : str
            'filename' child.
    
    """

    fluent_name = "export-modifications"

    argument_names = \
        ['command_list', 'filename']

    _child_classes = dict(
        command_list=command_list_cls,
        filename=filename_cls,
    )

    return_type = "<object object at 0x7f115b6aa800>"
