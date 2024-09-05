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


class max_vf_allowed_for_blocking(Real):
    """
    Set the maximum value for the DPM volume fraction used in the continuous flow when the volume displacement option is active.
     A default of 0.95 is recommendend.
    """

    fluent_name = "max-vf-allowed-for-blocking"

    return_type = "<object object at 0x7f115d64de20>"
