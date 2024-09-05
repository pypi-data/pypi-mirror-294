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


class skew_smooth_all_deforming_boundaries(Boolean):
    """
    Enable/disable skewness smoothing for all deforming 
    dynamic boundary zones. If disabled, only the deforming dynamic boundary zones are 
    smoothed which have smoothing explicitly enabled or use local face remeshing.
    """

    fluent_name = "skew-smooth-all-deforming-boundaries?"

