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

from .exclude_pairs import exclude_pairs as exclude_pairs_cls
from .exclusion_pairs import exclusion_pairs as exclusion_pairs_cls

class set_exclusion_pairs(Command):
    fluent_name = ...
    argument_names = ...
    exclude_pairs: exclude_pairs_cls = ...
    exclusion_pairs: exclusion_pairs_cls = ...
