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

from .parameterize_and_explore import parameterize_and_explore as parameterize_and_explore_cls
from .enable_21 import enable as enable_cls

class geometry(Group):
    """
    Geometry menu.
    """

    fluent_name = "geometry"

    child_names = \
        ['parameterize_and_explore']

    command_names = \
        ['enable']

    _child_classes = dict(
        parameterize_and_explore=parameterize_and_explore_cls,
        enable=enable_cls,
    )

