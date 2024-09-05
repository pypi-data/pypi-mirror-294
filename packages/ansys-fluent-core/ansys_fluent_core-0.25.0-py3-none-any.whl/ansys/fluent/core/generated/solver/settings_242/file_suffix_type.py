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


class file_suffix_type(String, AllowedValuesMixin):
    """
    Allows you to select flow-time, time-step, or crank-angle to be appended to the file name.
    """

    fluent_name = "file-suffix-type"

