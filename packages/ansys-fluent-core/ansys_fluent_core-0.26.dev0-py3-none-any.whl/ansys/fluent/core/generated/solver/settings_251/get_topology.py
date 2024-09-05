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

from .region_name import region_name as region_name_cls

class get_topology(Query):
    """
    Get topology.
    
    Parameters
    ----------
        region_name : str
            Sc region name.
    
    """

    fluent_name = "get-topology"

    argument_names = \
        ['region_name']

    _child_classes = dict(
        region_name=region_name_cls,
    )

