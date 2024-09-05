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

from .banded_1 import banded as banded_cls
from .smooth import smooth as smooth_cls

class colorings(Group):
    """
    'colorings' child.
    """

    fluent_name = "colorings"

    child_names = \
        ['banded', 'smooth']

    _child_classes = dict(
        banded=banded_cls,
        smooth=smooth_cls,
    )

