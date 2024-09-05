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

from .domain_val import domain_val as domain_val_cls

class element_mass_flow(Command):
    """
    'element_mass_flow' command.
    
    Parameters
    ----------
        domain_val : str
            'domain_val' child.
    
    """

    fluent_name = "element-mass-flow"

    argument_names = \
        ['domain_val']

    _child_classes = dict(
        domain_val=domain_val_cls,
    )

    return_type = "<object object at 0x7f115b49c440>"
