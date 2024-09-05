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

from .uds_bc_child import uds_bc_child


class pb_disc_bc(NamedObject[uds_bc_child], CreatableNamedObjectMixinOld[uds_bc_child]):
    fluent_name = ...
    child_object_type: uds_bc_child = ...
    return_type = ...
