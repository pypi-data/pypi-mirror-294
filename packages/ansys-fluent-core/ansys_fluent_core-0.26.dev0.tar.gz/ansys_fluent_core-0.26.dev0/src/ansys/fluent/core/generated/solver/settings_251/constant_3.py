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

from .diameter_4 import diameter as diameter_cls

class constant(Group):
    """
    'constant' child.
    """

    fluent_name = "constant"

    child_names = \
        ['diameter']

    _child_classes = dict(
        diameter=diameter_cls,
    )

