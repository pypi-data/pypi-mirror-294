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

from .write_flamelet_file import write_flamelet_file as write_flamelet_file_cls

class write_flamelet_cmd(Command):
    """
    Write a flamelet file.
    
    Parameters
    ----------
        write_flamelet_file : str
            Name Flamelet File.
    
    """

    fluent_name = "write-flamelet-cmd"

    argument_names = \
        ['write_flamelet_file']

    _child_classes = dict(
        write_flamelet_file=write_flamelet_file_cls,
    )

