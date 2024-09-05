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

from .turbulent_dispersion_1 import turbulent_dispersion as turbulent_dispersion_cls

class interphase_interactions(Group):
    """
    Enter the interphase interaction options menu.
    """

    fluent_name = "interphase-interactions"

    child_names = \
        ['turbulent_dispersion']

    _child_classes = dict(
        turbulent_dispersion=turbulent_dispersion_cls,
    )

