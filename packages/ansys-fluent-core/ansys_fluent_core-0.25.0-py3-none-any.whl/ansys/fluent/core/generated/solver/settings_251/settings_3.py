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

from .split_factor import split_factor as split_factor_cls
from .collapse_factor import collapse_factor as collapse_factor_cls
from .constant_height import constant_height as constant_height_cls

class settings(Group):
    """
    'settings' child.
    """

    fluent_name = "settings"

    child_names = \
        ['split_factor', 'collapse_factor', 'constant_height']

    _child_classes = dict(
        split_factor=split_factor_cls,
        collapse_factor=collapse_factor_cls,
        constant_height=constant_height_cls,
    )

