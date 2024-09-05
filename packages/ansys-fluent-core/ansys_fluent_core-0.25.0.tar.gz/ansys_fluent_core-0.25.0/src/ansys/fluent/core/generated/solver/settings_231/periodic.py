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

from .periodic_child import periodic_child


class periodic(NamedObject[periodic_child], _NonCreatableNamedObjectMixin[periodic_child]):
    """
    'periodic' child.
    """

    fluent_name = "periodic"

    child_object_type: periodic_child = periodic_child
    """
    child_object_type of periodic.
    """
    return_type = "<object object at 0x7f115c9feec0>"
