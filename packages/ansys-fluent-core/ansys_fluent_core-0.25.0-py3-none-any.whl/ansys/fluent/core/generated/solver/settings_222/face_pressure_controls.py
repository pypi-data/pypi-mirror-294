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

from .face_pressure_options import face_pressure_options as face_pressure_options_cls

class face_pressure_controls(Group):
    """
    'face_pressure_controls' child.
    """

    fluent_name = "face-pressure-controls"

    child_names = \
        ['face_pressure_options']

    _child_classes = dict(
        face_pressure_options=face_pressure_options_cls,
    )

    return_type = "<object object at 0x7f57023d17f0>"
