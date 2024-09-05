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

from .linearize import linearize as linearize_cls
from .threshold import threshold as threshold_cls

class continuity_transient_term_linearization(Group):
    fluent_name = ...
    child_names = ...
    linearize: linearize_cls = ...
    threshold: threshold_cls = ...
