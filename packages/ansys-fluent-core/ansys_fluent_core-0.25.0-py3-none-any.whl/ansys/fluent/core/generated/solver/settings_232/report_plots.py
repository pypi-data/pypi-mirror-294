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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .report_plots_child import report_plots_child


class report_plots(NamedObject[report_plots_child], CreatableNamedObjectMixinOld[report_plots_child]):
    """
    'report_plots' child.
    """

    fluent_name = "report-plots"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: report_plots_child = report_plots_child
    """
    child_object_type of report_plots.
    """
    return_type = "<object object at 0x7f641d662930>"
