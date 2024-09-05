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

from .moment_child import moment_child


class moment(NamedObject[moment_child], CreatableNamedObjectMixinOld[moment_child]):
    """
    'moment' child.
    """

    fluent_name = "moment"

    child_object_type: moment_child = moment_child
    """
    child_object_type of moment.
    """
    return_type = "<object object at 0x7f57023d2480>"
