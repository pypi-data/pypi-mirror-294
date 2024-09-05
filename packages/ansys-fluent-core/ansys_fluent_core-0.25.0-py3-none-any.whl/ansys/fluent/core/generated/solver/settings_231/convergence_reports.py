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

from .convergence_reports_child import convergence_reports_child


class convergence_reports(NamedObject[convergence_reports_child], CreatableNamedObjectMixinOld[convergence_reports_child]):
    """
    'convergence_reports' child.
    """

    fluent_name = "convergence-reports"

    child_object_type: convergence_reports_child = convergence_reports_child
    """
    child_object_type of convergence_reports.
    """
    return_type = "<object object at 0x7f115b6a94c0>"
