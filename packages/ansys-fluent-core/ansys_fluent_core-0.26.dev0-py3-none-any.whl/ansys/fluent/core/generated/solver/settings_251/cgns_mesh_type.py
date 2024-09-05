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


class cgns_mesh_type(String, AllowedValuesMixin):
    """
    Allows you to choose whether the mesh is mixed (default), its native format, or polyhedral.
    """

    fluent_name = "cgns-mesh-type"

