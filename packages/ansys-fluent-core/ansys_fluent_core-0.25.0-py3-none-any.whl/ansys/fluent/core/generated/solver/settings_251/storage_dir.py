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


class storage_dir(String, AllowedValuesMixin):
    """
    Specify the directory where animation images are stored using either an absolute or relative (./) path to currently opened case directory.
    """

    fluent_name = "storage-dir"

