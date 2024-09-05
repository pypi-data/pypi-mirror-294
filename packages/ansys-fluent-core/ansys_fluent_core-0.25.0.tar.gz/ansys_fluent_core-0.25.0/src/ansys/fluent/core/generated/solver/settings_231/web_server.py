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

from .start import start as start_cls
from .stop import stop as stop_cls

class web_server(Group):
    """
    'web_server' child.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop']

    _child_classes = dict(
        start=start_cls,
        stop=stop_cls,
    )

    return_type = "<object object at 0x7f115d64f530>"
