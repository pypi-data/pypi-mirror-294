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

from .droplet_particle_child import droplet_particle_child


class droplet_particle(NamedObject[droplet_particle_child], CreatableNamedObjectMixinOld[droplet_particle_child]):
    fluent_name = ...
    child_object_type: droplet_particle_child = ...
    return_type = ...
