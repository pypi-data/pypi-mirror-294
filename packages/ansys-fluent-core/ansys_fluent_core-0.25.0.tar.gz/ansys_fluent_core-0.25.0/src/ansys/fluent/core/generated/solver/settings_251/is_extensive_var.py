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

from .variable_name import variable_name as variable_name_cls

class is_extensive_var(Query):
    """
    Check for extensive var.
    
    Parameters
    ----------
        variable_name : str
            Sc variable name.
    
    """

    fluent_name = "is-extensive-var"

    argument_names = \
        ['variable_name']

    _child_classes = dict(
        variable_name=variable_name_cls,
    )

