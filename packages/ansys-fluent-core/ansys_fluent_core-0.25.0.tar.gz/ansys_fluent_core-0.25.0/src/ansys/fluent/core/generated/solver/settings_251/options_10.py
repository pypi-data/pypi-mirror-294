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

from .verbosity_15 import verbosity as verbosity_cls

class options(Group):
    """
    Enter AMG options menu.
    """

    fluent_name = "options"

    child_names = \
        ['verbosity']

    _child_classes = dict(
        verbosity=verbosity_cls,
    )

