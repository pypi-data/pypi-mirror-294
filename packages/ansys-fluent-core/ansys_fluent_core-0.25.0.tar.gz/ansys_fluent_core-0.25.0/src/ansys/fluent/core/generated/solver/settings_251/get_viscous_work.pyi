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

from .domain_2 import domain as domain_cls
from .zones_9 import zones as zones_cls
from .physics_2 import physics as physics_cls

class get_viscous_work(Query):
    fluent_name = ...
    argument_names = ...
    domain: domain_cls = ...
    zones: zones_cls = ...
    physics: physics_cls = ...
