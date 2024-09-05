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

from .compute import compute as compute_cls

class compute(Group):
    """
    'compute' child.
    """

    fluent_name = "compute"

    child_names = \
        ['compute']

    _child_classes = dict(
        compute=compute_cls,
    )

    return_type = "<object object at 0x7f57023d0360>"
