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

from .verbosity import verbosity as verbosity_cls

class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['verbosity']

    _child_classes = dict(
        verbosity=verbosity_cls,
    )

    return_type = "<object object at 0x7f57023d06f0>"
