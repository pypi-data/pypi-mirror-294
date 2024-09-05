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

from .report_plots_child import report_plots_child


class report_plots(NamedObject[report_plots_child], CreatableNamedObjectMixinOld[report_plots_child]):
    """
    'report_plots' child.
    """

    fluent_name = "report-plots"

    child_object_type: report_plots_child = report_plots_child
    """
    child_object_type of report_plots.
    """
    return_type = "<object object at 0x7f115b6a9390>"
