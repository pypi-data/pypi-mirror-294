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

from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls

class icing(Group):
    """
    Help not available.
    """

    fluent_name = "icing"

    child_names = \
        ['fensapice_flow_bc_subtype']

    _child_classes = dict(
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
    )

    return_type = "<object object at 0x7f5d09198340>"
