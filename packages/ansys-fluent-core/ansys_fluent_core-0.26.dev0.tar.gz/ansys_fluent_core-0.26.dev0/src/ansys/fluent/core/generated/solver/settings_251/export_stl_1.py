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

from .frequency_8 import frequency as frequency_cls
from .surfaces_19 import surfaces as surfaces_cls

class export_stl(Group):
    """
    Settings to export STL.
    """

    fluent_name = "export-stl"

    child_names = \
        ['frequency', 'surfaces']

    _child_classes = dict(
        frequency=frequency_cls,
        surfaces=surfaces_cls,
    )

