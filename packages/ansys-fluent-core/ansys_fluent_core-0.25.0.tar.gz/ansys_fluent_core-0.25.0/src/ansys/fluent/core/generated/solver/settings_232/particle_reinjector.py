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
from .time_delay import time_delay as time_delay_cls

class particle_reinjector(Group):
    """
    'particle_reinjector' child.
    """

    fluent_name = "particle-reinjector"

    child_names = \
        ['enable', 'time_delay']

    _child_classes = dict(
        enable=enable_cls,
        time_delay=time_delay_cls,
    )

    return_type = "<object object at 0x7f63fefe07b0>"
