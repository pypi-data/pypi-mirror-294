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

from .set_cgns_export_filetype import set_cgns_export_filetype as set_cgns_export_filetype_cls

class settings(Group):
    """
    Enter the export settings menu.
    """

    fluent_name = "settings"

    command_names = \
        ['set_cgns_export_filetype']

    _child_classes = dict(
        set_cgns_export_filetype=set_cgns_export_filetype_cls,
    )

    return_type = "<object object at 0x7f115d64e5c0>"
