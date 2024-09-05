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

class get_tensor_type(Query):
    """
    Get tensor type.
    
    Parameters
    ----------
        variable_name : str
            Sc variable name.
    
    """

    fluent_name = "get-tensor-type"

    argument_names = \
        ['variable_name']

    _child_classes = dict(
        variable_name=variable_name_cls,
    )

