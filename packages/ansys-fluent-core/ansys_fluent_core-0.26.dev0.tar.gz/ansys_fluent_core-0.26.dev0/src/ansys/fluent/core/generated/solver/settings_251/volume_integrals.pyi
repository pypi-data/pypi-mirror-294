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

from .mass_average import mass_average as mass_average_cls
from .mass_integral import mass_integral as mass_integral_cls
from .mass import mass as mass_cls
from .sum_1 import sum as sum_cls
from .twopisum import twopisum as twopisum_cls
from .minimum_5 import minimum as minimum_cls
from .maximum_5 import maximum as maximum_cls
from .volume_2 import volume as volume_cls
from .volume_average import volume_average as volume_average_cls
from .volume_integral import volume_integral as volume_integral_cls
from .get_mass_average import get_mass_average as get_mass_average_cls
from .get_mass_integral import get_mass_integral as get_mass_integral_cls
from .get_mass import get_mass as get_mass_cls
from .get_sum_1 import get_sum as get_sum_cls
from .get_twopisum import get_twopisum as get_twopisum_cls
from .get_minimum import get_minimum as get_minimum_cls
from .get_maximum import get_maximum as get_maximum_cls
from .get_volume import get_volume as get_volume_cls
from .get_volume_average import get_volume_average as get_volume_average_cls
from .compute_volume_integral import compute_volume_integral as compute_volume_integral_cls

class volume_integrals(Group):
    fluent_name = ...
    command_names = ...

    def mass_average(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-average of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def mass_integral(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-weighted integral of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def mass(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total mass of specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def sum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def twopisum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar over specified cell zones multiplied by 2*Pi.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def minimum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def maximum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def volume(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total volume of specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def volume_average(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume-weighted average of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def volume_integral(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume integral of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    query_names = ...

    def get_mass_average(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_mass_integral(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_mass(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_sum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_twopisum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_minimum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_maximum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_volume(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def get_volume_average(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

    def compute_volume_integral(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            cell_zones : List
                Volume id/name.
            volumes : List
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
        
        """

