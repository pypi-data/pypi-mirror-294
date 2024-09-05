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

from .surfaces_18 import surfaces as surfaces_cls

class delete_surfaces(Command):
    """
    Delete imported surfaces.
    
    Parameters
    ----------
        surfaces : List
            Surfaces to be deleted.
    
    """

    fluent_name = "delete-surfaces"

    argument_names = \
        ['surfaces']

    _child_classes = dict(
        surfaces=surfaces_cls,
    )

