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

from .zones_1 import zones as zones_cls

class display(Command):
    """
    Display specified mesh interface zone.
    
    Parameters
    ----------
        zones : List
            'zones' child.
    
    """

    fluent_name = "display"

    argument_names = \
        ['zones']

    _child_classes = dict(
        zones=zones_cls,
    )

    return_type = "<object object at 0x7f641d76a160>"
