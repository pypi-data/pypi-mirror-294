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

from .diagnosis import diagnosis as diagnosis_cls
from .match_fluent_flux_type import match_fluent_flux_type as match_fluent_flux_type_cls

class expert(Group):
    """
    Expert utilities menu.
    """

    fluent_name = "expert"

    child_names = \
        ['diagnosis', 'match_fluent_flux_type']

    _child_classes = dict(
        diagnosis=diagnosis_cls,
        match_fluent_flux_type=match_fluent_flux_type_cls,
    )

