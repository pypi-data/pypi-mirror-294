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

from .clear_current_instances import clear_current_instances as clear_current_instances_cls

class detect_surfaces(Command):
    """
    Detect the surfaces for the periodic instance.
    
    Parameters
    ----------
        clear_current_instances : bool
            Clear the current periodic instances.
    
    """

    fluent_name = "detect-surfaces"

    argument_names = \
        ['clear_current_instances']

    _child_classes = dict(
        clear_current_instances=clear_current_instances_cls,
    )

