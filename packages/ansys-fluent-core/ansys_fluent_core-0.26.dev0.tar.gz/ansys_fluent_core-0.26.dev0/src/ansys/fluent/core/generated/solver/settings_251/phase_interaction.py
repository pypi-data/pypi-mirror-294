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

from .forces import forces as forces_cls

class phase_interaction(Group):
    """
    Specify phase interaction.
    """

    fluent_name = "phase-interaction"

    child_names = \
        ['forces']

    _child_classes = dict(
        forces=forces_cls,
    )

