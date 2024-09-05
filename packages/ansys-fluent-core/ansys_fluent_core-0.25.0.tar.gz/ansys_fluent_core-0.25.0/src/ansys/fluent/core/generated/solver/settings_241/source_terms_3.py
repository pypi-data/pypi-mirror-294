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

from .sources import sources as sources_cls
from .source_terms_2 import source_terms as source_terms_cls

class source_terms(Group):
    """
    Help not available.
    """

    fluent_name = "source-terms"

    child_names = \
        ['sources', 'source_terms']

    _child_classes = dict(
        sources=sources_cls,
        source_terms=source_terms_cls,
    )

    return_type = "<object object at 0x7f5d08b049d0>"
