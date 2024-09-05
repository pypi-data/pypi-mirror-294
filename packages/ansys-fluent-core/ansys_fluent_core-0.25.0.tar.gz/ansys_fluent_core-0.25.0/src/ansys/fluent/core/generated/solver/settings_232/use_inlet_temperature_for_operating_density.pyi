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

from .zone_name import zone_name as zone_name_cls

class use_inlet_temperature_for_operating_density(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    return_type = ...
