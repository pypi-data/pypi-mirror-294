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

from .material_5 import material as material_cls
from .participates_in_radiation import participates_in_radiation as participates_in_radiation_cls

class general(Group):
    """
    Allows to change general model variables or settings.
    """

    fluent_name = "general"

    child_names = \
        ['material', 'participates_in_radiation']

    _child_classes = dict(
        material=material_cls,
        participates_in_radiation=participates_in_radiation_cls,
    )

    _child_aliases = dict(
        radiating="participates_in_radiation",
    )

