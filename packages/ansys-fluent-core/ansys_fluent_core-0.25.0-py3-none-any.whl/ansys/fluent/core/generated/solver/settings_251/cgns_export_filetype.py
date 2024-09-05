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


class cgns_export_filetype(String, AllowedValuesMixin):
    """
    Select HDF5 or ADF as file format for CGNS.
    """

    fluent_name = "cgns-export-filetype"

