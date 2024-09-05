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

from .option_5 import option as option_cls
from .expression_1 import expression as expression_cls
from .user_defined_2 import user_defined as user_defined_cls

class blending_function(Group):
    """
    Set the GEKO model blending function.
    """

    fluent_name = "blending-function"

    child_names = \
        ['option', 'expression', 'user_defined']

    _child_classes = dict(
        option=option_cls,
        expression=expression_cls,
        user_defined=user_defined_cls,
    )

