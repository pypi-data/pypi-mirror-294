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

from .gradient_based import gradient_based as gradient_based_cls
from .geometry_9 import geometry as geometry_cls

class design(Group):
    """
    'design' child.
    """

    fluent_name = "design"

    child_names = \
        ['gradient_based', 'geometry']

    _child_classes = dict(
        gradient_based=gradient_based_cls,
        geometry=geometry_cls,
    )

