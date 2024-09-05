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

from .under_relaxation_factor import under_relaxation_factor as under_relaxation_factor_cls
from .explicit_relaxation_factor import explicit_relaxation_factor as explicit_relaxation_factor_cls

class expert(Group):
    """
    Enter menu for expert controls.
    """

    fluent_name = "expert"

    child_names = \
        ['under_relaxation_factor', 'explicit_relaxation_factor']

    _child_classes = dict(
        under_relaxation_factor=under_relaxation_factor_cls,
        explicit_relaxation_factor=explicit_relaxation_factor_cls,
    )

    return_type = "<object object at 0x7f115b7b6c00>"
