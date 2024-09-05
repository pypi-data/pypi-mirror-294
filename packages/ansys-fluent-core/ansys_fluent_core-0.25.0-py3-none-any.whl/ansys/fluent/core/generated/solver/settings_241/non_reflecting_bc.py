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

from .general_nrbc import general_nrbc as general_nrbc_cls
from .turbo_sepcific_nrbc import turbo_sepcific_nrbc as turbo_sepcific_nrbc_cls

class non_reflecting_bc(Group):
    """
    'non_reflecting_bc' child.
    """

    fluent_name = "non-reflecting-bc"

    child_names = \
        ['general_nrbc', 'turbo_sepcific_nrbc']

    _child_classes = dict(
        general_nrbc=general_nrbc_cls,
        turbo_sepcific_nrbc=turbo_sepcific_nrbc_cls,
    )

    return_type = "<object object at 0x7f5cfbb850d0>"
