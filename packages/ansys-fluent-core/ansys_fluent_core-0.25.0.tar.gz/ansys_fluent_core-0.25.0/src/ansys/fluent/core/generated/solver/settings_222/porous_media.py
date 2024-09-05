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

from .relative_permeability import relative_permeability as relative_permeability_cls

class porous_media(Group):
    """
    'porous_media' child.
    """

    fluent_name = "porous-media"

    child_names = \
        ['relative_permeability']

    _child_classes = dict(
        relative_permeability=relative_permeability_cls,
    )

    return_type = "<object object at 0x7f57023d1210>"
