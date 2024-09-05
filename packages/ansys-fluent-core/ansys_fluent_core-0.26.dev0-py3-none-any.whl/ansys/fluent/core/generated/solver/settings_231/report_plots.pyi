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

from .report_plots_child import report_plots_child


class report_plots(NamedObject[report_plots_child], CreatableNamedObjectMixinOld[report_plots_child]):
    fluent_name = ...
    child_object_type: report_plots_child = ...
    return_type = ...
