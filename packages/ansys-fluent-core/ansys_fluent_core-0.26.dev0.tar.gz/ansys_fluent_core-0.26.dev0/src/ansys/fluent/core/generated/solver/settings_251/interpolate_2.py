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

from .export_data_1 import export_data as export_data_cls
from .import_data_1 import import_data as import_data_cls

class interpolate(Group):
    """
    Interpolation utilities menu.
    """

    fluent_name = "interpolate"

    command_names = \
        ['export_data', 'import_data']

    _child_classes = dict(
        export_data=export_data_cls,
        import_data=import_data_cls,
    )

