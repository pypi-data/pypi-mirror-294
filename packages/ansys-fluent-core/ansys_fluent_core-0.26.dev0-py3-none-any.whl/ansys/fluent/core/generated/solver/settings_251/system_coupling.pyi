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
    fluent_name = ...
    child_names = ...
    htc: htc_cls = ...
    unsteady_statistics: unsteady_statistics_cls = ...
    user_defined_coupling_variables_via_udm: user_defined_coupling_variables_via_udm_cls = ...
    use_face_or_element_based_data_transfer: use_face_or_element_based_data_transfer_cls = ...
    flow_boundary_coupling: flow_boundary_coupling_cls = ...
    command_names = ...

    def write_scp_file(self, file_name: str):
        """
        Write fluent input scp file for sc.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def connect_parallel(self, schost: str, scport: int, scname: str):
        """
        System coupling connection status.
        
        Parameters
        ----------
            schost : str
                Sc solver host input.
            scport : int
                Sc solver port input.
            scname : str
                Sc solver name input.
        
        """

    def init_and_solve(self, ):
        """
        System-coupling-solve-init-command.
        """

    def solve(self, ):
        """
        System-coupling-solve-command.
        """

    query_names = ...

    def get_analysis_type(self, ):
        """
        Get analysis type.
        """

    def get_all_regions(self, ):
        """
        Get all supported sc regions.
        """

    def get_topology(self, region_name: str):
        """
        Get topology.
        
        Parameters
        ----------
            region_name : str
                Sc region name.
        
        """

    def get_input_vars(self, region_name: str):
        """
        Get input vars for a given region.
        
        Parameters
        ----------
            region_name : str
                Sc region name.
        
        """

    def get_output_vars(self, region_name: str):
        """
        Get output vars for a given region.
        
        Parameters
        ----------
            region_name : str
                Sc region name.
        
        """

    def is_extensive_var(self, variable_name: str):
        """
        Check for extensive var.
        
        Parameters
        ----------
            variable_name : str
                Sc variable name.
        
        """

    def get_data_location(self, variable_name: str):
        """
        Get data location.
        
        Parameters
        ----------
            variable_name : str
                Sc variable name.
        
        """

    def get_tensor_type(self, variable_name: str):
        """
        Get tensor type.
        
        Parameters
        ----------
            variable_name : str
                Sc variable name.
        
        """

