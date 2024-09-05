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

from .coupled_level_set import coupled_level_set as coupled_level_set_cls

class hybrid_models(Group):
    """
    Hybrid models.
    """

    fluent_name = "hybrid-models"

    child_names = \
        ['coupled_level_set']

    _child_classes = dict(
        coupled_level_set=coupled_level_set_cls,
    )

