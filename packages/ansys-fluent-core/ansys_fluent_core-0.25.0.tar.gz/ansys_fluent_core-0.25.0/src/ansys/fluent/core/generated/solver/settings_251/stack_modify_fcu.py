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

from .fcu_name import fcu_name as fcu_name_cls
from .cellzones_2 import cellzones as cellzones_cls

class stack_modify_fcu(Command):
    """
    Modify stack units.
    
    Parameters
    ----------
        fcu_name : str
            Name of fcu.
        cellzones : List
            Enter cell zones.
    
    """

    fluent_name = "stack-modify-fcu"

    argument_names = \
        ['fcu_name', 'cellzones']

    _child_classes = dict(
        fcu_name=fcu_name_cls,
        cellzones=cellzones_cls,
    )

