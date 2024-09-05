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

from .option_10 import option as option_cls

class turbulence_chemistry_interaction(Group):
    """
    Turbulence-Chemistry Interaction.
    """

    fluent_name = "turbulence-chemistry-interaction"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

