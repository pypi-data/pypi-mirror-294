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


class vapor_phase_realgas(Integer, AllowedValuesMixin):
    """
    Set zone real-gas state:
    
    	-1:use global setting
    
    	 0:liquid
    	 1:vapor.
    """

    fluent_name = "vapor-phase-realgas"

    return_type = "<object object at 0x7f5d08aaf580>"
