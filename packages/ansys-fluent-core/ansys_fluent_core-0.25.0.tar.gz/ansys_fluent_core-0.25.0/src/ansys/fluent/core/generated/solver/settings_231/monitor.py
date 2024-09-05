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

from .report_files import report_files as report_files_cls
from .report_plots import report_plots as report_plots_cls
from .convergence_conditions import convergence_conditions as convergence_conditions_cls

class monitor(Group):
    """
    'monitor' child.
    """

    fluent_name = "monitor"

    child_names = \
        ['report_files', 'report_plots', 'convergence_conditions']

    _child_classes = dict(
        report_files=report_files_cls,
        report_plots=report_plots_cls,
        convergence_conditions=convergence_conditions_cls,
    )

    return_type = "<object object at 0x7f115b6a9630>"
