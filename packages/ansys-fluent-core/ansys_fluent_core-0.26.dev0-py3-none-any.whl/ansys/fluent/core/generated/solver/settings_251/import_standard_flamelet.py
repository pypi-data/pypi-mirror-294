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

from .standard_flamelet_file import standard_flamelet_file as standard_flamelet_file_cls

class import_standard_flamelet(Command):
    """
    Import Standard Flamelet.
    
    Parameters
    ----------
        standard_flamelet_file : List
            Import Standard Flamelet File.
    
    """

    fluent_name = "import-standard-flamelet"

    argument_names = \
        ['standard_flamelet_file']

    _child_classes = dict(
        standard_flamelet_file=standard_flamelet_file_cls,
    )

