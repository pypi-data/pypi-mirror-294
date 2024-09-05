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

from .name import name as name_cls

class icemcfd_for_icepak(Command):
    """
    Write a binary ICEMCFD domain file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "icemcfd-for-icepak"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

    return_type = "<object object at 0x7f115d64e770>"
