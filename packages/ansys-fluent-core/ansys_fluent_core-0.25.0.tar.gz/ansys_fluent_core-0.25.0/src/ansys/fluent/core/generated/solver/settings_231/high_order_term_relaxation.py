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

from .enable_5 import enable as enable_cls
from .options_3 import options as options_cls

class high_order_term_relaxation(Group):
    """
    Enter High Order Relaxation Menu.
    """

    fluent_name = "high-order-term-relaxation"

    child_names = \
        ['enable', 'options']

    _child_classes = dict(
        enable=enable_cls,
        options=options_cls,
    )

    return_type = "<object object at 0x7f115b7b7ab0>"
