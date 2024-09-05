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

from typing import Union, List, Tuple

from .mf_1 import mf as mf_cls
from .urf_1 import urf as urf_cls

class solution_controls(Command):
    fluent_name = ...
    argument_names = ...
    mf: mf_cls = ...
    urf: urf_cls = ...
    return_type = ...
