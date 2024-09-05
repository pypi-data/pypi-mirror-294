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

from .original_surfaces import original_surfaces as original_surfaces_cls

class display_imported_surfaces(Command):
    """
    Display imported surfaces.
    
    Parameters
    ----------
        original_surfaces : List
            Select surface.
    
    """

    fluent_name = "display-imported-surfaces"

    argument_names = \
        ['original_surfaces']

    _child_classes = dict(
        original_surfaces=original_surfaces_cls,
    )

