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

from .injection_child import injection_child


class injection(NamedObject[injection_child], CreatableNamedObjectMixinOld[injection_child]):
    """
    'injection' child.
    """

    fluent_name = "injection"

    child_object_type: injection_child = injection_child
    """
    child_object_type of injection.
    """
    return_type = "<object object at 0x7f115b6a8de0>"
