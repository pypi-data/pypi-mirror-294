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

from .expression_child import expression_child


class expression(NamedObject[expression_child], CreatableNamedObjectMixinOld[expression_child]):
    fluent_name = ...
    child_object_type: expression_child = ...
    return_type = ...
