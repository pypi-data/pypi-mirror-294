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

from .from_ import from_ as from__cls
from .to_1 import to as to_cls
from .verbosity_3 import verbosity as verbosity_cls

class copy(Command):
    """
    'copy' command.
    
    Parameters
    ----------
        from_ : str
            'from' child.
        to : List
            'to' child.
        verbosity : bool
            'verbosity' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['from_', 'to', 'verbosity']

    _child_classes = dict(
        from_=from__cls,
        to=to_cls,
        verbosity=verbosity_cls,
    )

    return_type = "<object object at 0x7f641e98c730>"
