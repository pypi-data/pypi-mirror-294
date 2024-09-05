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


class reference_frame(String, AllowedValuesMixin):
    """
    Enable/disable tracking of particles in the absolute frame. Please note that tracking in the relative frame is the recommended default.
    """

    fluent_name = "reference-frame"

