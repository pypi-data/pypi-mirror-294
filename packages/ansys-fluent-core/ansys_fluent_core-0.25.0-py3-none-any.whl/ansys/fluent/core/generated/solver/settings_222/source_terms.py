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

from .source_terms_child import source_terms_child


class source_terms(NamedObject[source_terms_child], CreatableNamedObjectMixinOld[source_terms_child]):
    """
    'source_terms' child.
    """

    fluent_name = "source-terms"

    child_object_type: source_terms_child = source_terms_child
    """
    child_object_type of source_terms.
    """
    return_type = "<object object at 0x7f570357de30>"
