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

from .convergence_reports_child import convergence_reports_child


class convergence_reports(NamedObject[convergence_reports_child], CreatableNamedObjectMixinOld[convergence_reports_child]):
    fluent_name = ...
    child_object_type: convergence_reports_child = ...
    return_type = ...
