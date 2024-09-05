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

from .mesh_child import mesh_child


class mesh(NamedObject[mesh_child], CreatableNamedObjectMixinOld[mesh_child]):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    child_object_type: mesh_child = mesh_child
    """
    child_object_type of mesh.
    """
    return_type = "<object object at 0x7f115b6a8660>"
