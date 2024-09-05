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


class cell_zones(StringList, AllowedValuesMixin):
    """
    Specify names or IDs of cell zones to be copied. If an empty list is given, all active cell zones will be copied.
    """

    fluent_name = "cell-zones"

