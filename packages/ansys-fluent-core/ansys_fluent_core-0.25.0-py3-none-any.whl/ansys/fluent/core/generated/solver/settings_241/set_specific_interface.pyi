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

from typing import Union, List, Tuple

from .interface_number import interface_number as interface_number_cls
from .bands import bands as bands_cls

class set_specific_interface(Command):
    fluent_name = ...
    argument_names = ...
    interface_number: interface_number_cls = ...
    bands: bands_cls = ...
    return_type = ...
