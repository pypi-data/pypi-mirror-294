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

from .enabled_40 import enabled as enabled_cls
from .settings_2 import settings as settings_cls

class remeshing(Group):
    """
    'remeshing' child.
    """

    fluent_name = "remeshing"

    child_names = \
        ['enabled', 'settings']

    _child_classes = dict(
        enabled=enabled_cls,
        settings=settings_cls,
    )

