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

from .disk_child import disk_child


class disk(NamedObject[disk_child], CreatableNamedObjectMixinOld[disk_child]):
    """
    Main menu to define a rotor disk:
    
     - delete : delete a vbm disk
     - edit   : edit a vbm disk
     - new    : create a new vbm disk
     - rename : rename a vbm disk.
    
    """

    fluent_name = "disk"

    child_object_type: disk_child = disk_child
    """
    child_object_type of disk.
    """
    return_type = "<object object at 0x7f115d64cf60>"
