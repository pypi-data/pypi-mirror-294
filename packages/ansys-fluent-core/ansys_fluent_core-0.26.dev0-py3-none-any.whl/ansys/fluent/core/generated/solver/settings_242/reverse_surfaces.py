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

from .surfaces_16 import surfaces as surfaces_cls

class reverse_surfaces(Command):
    """
    Reverse selected surfaces.
    
    Parameters
    ----------
        surfaces : List
            Surfaces orientations to be reverse.
    
    """

    fluent_name = "reverse-surfaces"

    argument_names = \
        ['surfaces']

    _child_classes = dict(
        surfaces=surfaces_cls,
    )

