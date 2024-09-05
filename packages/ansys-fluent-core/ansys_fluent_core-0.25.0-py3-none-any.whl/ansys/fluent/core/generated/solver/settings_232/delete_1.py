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

from .si_delete import si_delete as si_delete_cls

class delete(CommandWithPositionalArgs):
    """
    Delete a mesh interface.
    
    Parameters
    ----------
        si_delete : str
            'si_delete' child.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['si_delete']

    _child_classes = dict(
        si_delete=si_delete_cls,
    )

    return_type = "<object object at 0x7f641d76a120>"
