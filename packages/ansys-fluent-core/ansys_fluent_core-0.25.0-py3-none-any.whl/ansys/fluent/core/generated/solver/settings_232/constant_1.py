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

from .diameter_1 import diameter as diameter_cls

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

    return_type = "<object object at 0x7f641d5530c0>"
