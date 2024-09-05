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

from .monitor_4 import monitor as monitor_cls

class monitor(Command):
    """
    Transient monitor.
    
    Parameters
    ----------
        monitor : List
            Select report file name(s) for transient monitor.
    
    """

    fluent_name = "monitor"

    argument_names = \
        ['monitor']

    _child_classes = dict(
        monitor=monitor_cls,
    )

