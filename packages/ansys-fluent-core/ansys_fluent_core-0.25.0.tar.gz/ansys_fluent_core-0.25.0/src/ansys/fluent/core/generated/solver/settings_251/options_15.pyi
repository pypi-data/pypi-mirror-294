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

from .auto_scale import auto_scale as auto_scale_cls
from .vector_style import vector_style as vector_style_cls
from .scale_3 import scale as scale_cls
from .skip import skip as skip_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    auto_scale: auto_scale_cls = ...
    vector_style: vector_style_cls = ...
    scale: scale_cls = ...
    skip: skip_cls = ...
