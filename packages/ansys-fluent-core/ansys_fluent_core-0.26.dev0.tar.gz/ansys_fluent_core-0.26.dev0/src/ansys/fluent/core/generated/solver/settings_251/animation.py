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

from .animate import animate as animate_cls

class animation(Command):
    """
    Create transient animation(s).
    
    Parameters
    ----------
        animate : List
            Select animation object name(s) for transient animation.
    
    """

    fluent_name = "animation"

    argument_names = \
        ['animate']

    _child_classes = dict(
        animate=animate_cls,
    )

