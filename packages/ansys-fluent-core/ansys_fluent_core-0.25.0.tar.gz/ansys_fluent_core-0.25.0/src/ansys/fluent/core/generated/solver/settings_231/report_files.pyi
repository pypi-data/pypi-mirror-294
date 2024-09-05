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

from .report_files_child import report_files_child


class report_files(NamedObject[report_files_child], CreatableNamedObjectMixinOld[report_files_child]):
    fluent_name = ...
    child_object_type: report_files_child = ...
    return_type = ...
