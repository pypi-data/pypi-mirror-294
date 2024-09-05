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

from .begin import begin as begin_cls
from .end_1 import end as end_cls
from .increment_3 import increment as increment_cls

class uniform(Command):
    fluent_name = ...
    argument_names = ...
    begin: begin_cls = ...
    end: end_cls = ...
    increment: increment_cls = ...
