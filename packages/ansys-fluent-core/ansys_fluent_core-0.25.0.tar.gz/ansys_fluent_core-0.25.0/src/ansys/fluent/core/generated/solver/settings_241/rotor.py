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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .rotor_child import rotor_child


class rotor(NamedObject[rotor_child], CreatableNamedObjectMixinOld[rotor_child]):
    """
    Main menu to define a rotor disk:
    
     - delete : delete a vbm disk
     - edit   : edit a vbm disk
     - new    : create a new vbm disk
     - rename : rename a vbm disk.
    
    """

    fluent_name = "rotor"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: rotor_child = rotor_child
    """
    child_object_type of rotor.
    """
    return_type = "<object object at 0x7f5ce12d63a0>"
