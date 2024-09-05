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

from .injection_names import injection_names as injection_names_cls

class particle_summary(Command):
    """
    Print summary report for all current particles.
    
    Parameters
    ----------
        injection_names : List
            'injection_names' child.
    
    """

    fluent_name = "particle-summary"

    argument_names = \
        ['injection_names']

    _child_classes = dict(
        injection_names=injection_names_cls,
    )

