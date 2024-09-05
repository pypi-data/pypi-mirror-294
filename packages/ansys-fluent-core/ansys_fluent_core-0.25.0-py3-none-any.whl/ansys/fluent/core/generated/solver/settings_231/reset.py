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

from .reset_color import reset_color as reset_color_cls

class reset(Command):
    """
    To reset colors and/or materials to the defaults.
    
    Parameters
    ----------
        reset_color : bool
            'reset_color' child.
    
    """

    fluent_name = "reset?"

    argument_names = \
        ['reset_color']

    _child_classes = dict(
        reset_color=reset_color_cls,
    )

    return_type = "<object object at 0x7f115b5a1db0>"
