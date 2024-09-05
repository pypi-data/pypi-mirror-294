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

from .turbulence_options import turbulence_options as turbulence_options_cls
from .enable_13 import enable as enable_cls

class warped_face_gradient_correction(Group):
    """
    Enter warped-face-gradient-correction menu.
    """

    fluent_name = "warped-face-gradient-correction"

    child_names = \
        ['turbulence_options']

    command_names = \
        ['enable']

    _child_classes = dict(
        turbulence_options=turbulence_options_cls,
        enable=enable_cls,
    )

    return_type = "<object object at 0x7f641d76bdc0>"
