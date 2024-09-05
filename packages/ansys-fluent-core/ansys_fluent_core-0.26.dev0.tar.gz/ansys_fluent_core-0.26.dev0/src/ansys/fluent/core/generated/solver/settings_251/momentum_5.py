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

from .flowrate_frac import flowrate_frac as flowrate_frac_cls

class momentum(Group):
    """
    Allows to change momentum model variables or settings.
    """

    fluent_name = "momentum"

    child_names = \
        ['flowrate_frac']

    _child_classes = dict(
        flowrate_frac=flowrate_frac_cls,
    )

