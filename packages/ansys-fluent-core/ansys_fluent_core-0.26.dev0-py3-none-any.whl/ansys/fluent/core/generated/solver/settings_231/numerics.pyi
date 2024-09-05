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

from .averaging import averaging as averaging_cls
from .source_terms import source_terms as source_terms_cls
from .tracking import tracking as tracking_cls

class numerics(Group):
    fluent_name = ...
    child_names = ...
    averaging: averaging_cls = ...
    source_terms: source_terms_cls = ...
    tracking: tracking_cls = ...
    return_type = ...
