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

from .rif_prp_file import rif_prp_file as rif_prp_file_cls
from .rif_flamelet_file import rif_flamelet_file as rif_flamelet_file_cls

class import_rif_flamelet(Command):
    fluent_name = ...
    argument_names = ...
    rif_prp_file: rif_prp_file_cls = ...
    rif_flamelet_file: rif_flamelet_file_cls = ...
