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

from .domain import domain as domain_cls

class element_mass_flow(Command):
    """
    'element_mass_flow' command.
    
    Parameters
    ----------
        domain : str
            'domain' child.
    
    """

    fluent_name = "element-mass-flow"

    argument_names = \
        ['domain']

    _child_classes = dict(
        domain=domain_cls,
    )

    return_type = "<object object at 0x7f5cfb7b1f00>"
