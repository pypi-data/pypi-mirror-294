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

from .begin import begin as begin_cls
from .end_1 import end as end_cls
from .increment_3 import increment as increment_cls

class uniform(Command):
    """
    Select begin, end and increment for timestep selection.
    
    Parameters
    ----------
        begin : int
            Select begin-timestep for timestep-selector.
        end : int
            Select end-timestep for timestep-selector.
        increment : int
            Select increment for timestep-selector.
    
    """

    fluent_name = "uniform"

    argument_names = \
        ['begin', 'end', 'increment']

    _child_classes = dict(
        begin=begin_cls,
        end=end_cls,
        increment=increment_cls,
    )

