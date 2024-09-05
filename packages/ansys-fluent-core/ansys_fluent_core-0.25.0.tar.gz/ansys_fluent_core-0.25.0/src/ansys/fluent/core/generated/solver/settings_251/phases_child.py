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

from .name import name as name_cls
from .material import material as material_cls

class phases_child(Group):
    """
    'child_object_type' of phases.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'material']

    _child_classes = dict(
        name=name_cls,
        material=material_cls,
    )

