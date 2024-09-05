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

from .bodies import bodies as bodies_cls
from .groups import groups as groups_cls

class parts_child(Group):
    """
    'child_object_type' of parts.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['bodies', 'groups']

    _child_classes = dict(
        bodies=bodies_cls,
        groups=groups_cls,
    )

    return_type = "<object object at 0x7f641d76a720>"
