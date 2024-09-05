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

from .unified_remeshing import unified_remeshing as unified_remeshing_cls
from .cell_skew_max import cell_skew_max as cell_skew_max_cls
from .face_skew_max import face_skew_max as face_skew_max_cls
from .retain_size_distribution import retain_size_distribution as retain_size_distribution_cls
from .length_min import length_min as length_min_cls
from .length_max import length_max as length_max_cls

class settings(Group):
    fluent_name = ...
    child_names = ...
    unified_remeshing: unified_remeshing_cls = ...
    cell_skew_max: cell_skew_max_cls = ...
    face_skew_max: face_skew_max_cls = ...
    retain_size_distribution: retain_size_distribution_cls = ...
    length_min: length_min_cls = ...
    length_max: length_max_cls = ...
