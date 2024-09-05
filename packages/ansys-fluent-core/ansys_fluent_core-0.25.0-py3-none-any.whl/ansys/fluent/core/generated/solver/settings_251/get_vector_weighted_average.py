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

from .surface_names_2 import surface_names as surface_names_cls
from .geometry_names import geometry_names as geometry_names_cls
from .cust_vec_func import cust_vec_func as cust_vec_func_cls
from .report_of import report_of as report_of_cls
from .current_domain import current_domain as current_domain_cls

class get_vector_weighted_average(Query):
    """
    Create a surface integral report.
    
    Parameters
    ----------
        surface_names : List
            Select surface.
        geometry_names : List
            Select UTL Geometry.
        cust_vec_func : str
            Specify the custom vectors.
        report_of : str
            Specify Field.
        current_domain : str
            Select the domain.
    
    """

    fluent_name = "get-vector-weighted-average"

    argument_names = \
        ['surface_names', 'geometry_names', 'cust_vec_func', 'report_of',
         'current_domain']

    _child_classes = dict(
        surface_names=surface_names_cls,
        geometry_names=geometry_names_cls,
        cust_vec_func=cust_vec_func_cls,
        report_of=report_of_cls,
        current_domain=current_domain_cls,
    )

