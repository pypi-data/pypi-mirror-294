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

from .htc import htc as htc_cls
from .unsteady_statistics import unsteady_statistics as unsteady_statistics_cls
from .user_defined_coupling_variables_via_udm import user_defined_coupling_variables_via_udm as user_defined_coupling_variables_via_udm_cls
from .use_face_or_element_based_data_transfer import use_face_or_element_based_data_transfer as use_face_or_element_based_data_transfer_cls
from .flow_boundary_coupling import flow_boundary_coupling as flow_boundary_coupling_cls
from .write_scp_file import write_scp_file as write_scp_file_cls
from .connect_parallel import connect_parallel as connect_parallel_cls
from .init_and_solve import init_and_solve as init_and_solve_cls
from .solve import solve as solve_cls
from .get_analysis_type import get_analysis_type as get_analysis_type_cls
from .get_all_regions import get_all_regions as get_all_regions_cls
from .get_topology import get_topology as get_topology_cls
from .get_input_vars import get_input_vars as get_input_vars_cls
from .get_output_vars import get_output_vars as get_output_vars_cls
from .is_extensive_var import is_extensive_var as is_extensive_var_cls
from .get_data_location import get_data_location as get_data_location_cls
from .get_tensor_type import get_tensor_type as get_tensor_type_cls

class system_coupling(Group):
    """
    Enter the system coupling model menu.
    """

    fluent_name = "system-coupling"

    child_names = \
        ['htc', 'unsteady_statistics',
         'user_defined_coupling_variables_via_udm',
         'use_face_or_element_based_data_transfer', 'flow_boundary_coupling']

    command_names = \
        ['write_scp_file', 'connect_parallel', 'init_and_solve', 'solve']

    query_names = \
        ['get_analysis_type', 'get_all_regions', 'get_topology',
         'get_input_vars', 'get_output_vars', 'is_extensive_var',
         'get_data_location', 'get_tensor_type']

    _child_classes = dict(
        htc=htc_cls,
        unsteady_statistics=unsteady_statistics_cls,
        user_defined_coupling_variables_via_udm=user_defined_coupling_variables_via_udm_cls,
        use_face_or_element_based_data_transfer=use_face_or_element_based_data_transfer_cls,
        flow_boundary_coupling=flow_boundary_coupling_cls,
        write_scp_file=write_scp_file_cls,
        connect_parallel=connect_parallel_cls,
        init_and_solve=init_and_solve_cls,
        solve=solve_cls,
        get_analysis_type=get_analysis_type_cls,
        get_all_regions=get_all_regions_cls,
        get_topology=get_topology_cls,
        get_input_vars=get_input_vars_cls,
        get_output_vars=get_output_vars_cls,
        is_extensive_var=is_extensive_var_cls,
        get_data_location=get_data_location_cls,
        get_tensor_type=get_tensor_type_cls,
    )

