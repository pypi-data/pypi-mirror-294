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

from .sources import sources as sources_cls
from .source_terms_2 import source_terms as source_terms_cls

class source_terms(Group):
    fluent_name = ...
    child_names = ...
    sources: sources_cls = ...
    source_terms: source_terms_cls = ...
    return_type = ...
