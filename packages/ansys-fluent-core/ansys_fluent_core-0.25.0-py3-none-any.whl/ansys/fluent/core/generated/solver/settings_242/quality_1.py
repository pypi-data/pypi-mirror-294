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


class quality(String, AllowedValuesMixin):
    """
    Set the quality for raytracing. Higher quality leads to more refining of the raytraced image, which results in more time and memory consumption.
    """

    fluent_name = "quality"

