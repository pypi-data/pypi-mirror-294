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


class backplate_image(String, AllowedValuesMixin):
    """
    Set the backplate image. This will override the backplate color unless the image is set to 'none'.
    """

    fluent_name = "backplate-image"

