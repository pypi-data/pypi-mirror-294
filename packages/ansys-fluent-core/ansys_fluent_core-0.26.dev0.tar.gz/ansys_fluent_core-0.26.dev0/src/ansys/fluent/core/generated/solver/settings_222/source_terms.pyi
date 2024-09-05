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

from .source_terms_child import source_terms_child


class source_terms(NamedObject[source_terms_child], CreatableNamedObjectMixinOld[source_terms_child]):
    fluent_name = ...
    child_object_type: source_terms_child = ...
    return_type = ...
