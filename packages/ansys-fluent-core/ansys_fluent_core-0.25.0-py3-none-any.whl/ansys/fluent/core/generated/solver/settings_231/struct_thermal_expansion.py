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

from .option_10 import option as option_cls
from .value import value as value_cls
from .orthotropic_structure_te import orthotropic_structure_te as orthotropic_structure_te_cls

class struct_thermal_expansion(Group):
    """
    'struct_thermal_expansion' child.
    """

    fluent_name = "struct-thermal-expansion"

    child_names = \
        ['option', 'value', 'orthotropic_structure_te']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        orthotropic_structure_te=orthotropic_structure_te_cls,
    )

    return_type = "<object object at 0x7f115c1a49b0>"
