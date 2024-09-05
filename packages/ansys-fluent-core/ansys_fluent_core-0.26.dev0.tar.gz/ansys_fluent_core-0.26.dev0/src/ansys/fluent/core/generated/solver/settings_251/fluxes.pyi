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

from .mass_flow_1 import mass_flow as mass_flow_cls
from .heat_transfer import heat_transfer as heat_transfer_cls
from .heat_transfer_sensible import heat_transfer_sensible as heat_transfer_sensible_cls
from .radiation_heat_transfer import radiation_heat_transfer as radiation_heat_transfer_cls
from .film_mass_flow import film_mass_flow as film_mass_flow_cls
from .film_heat_transfer import film_heat_transfer as film_heat_transfer_cls
from .electric_current import electric_current as electric_current_cls
from .pressure_work_1 import pressure_work as pressure_work_cls
from .viscous_work import viscous_work as viscous_work_cls
from .get_mass_flow import get_mass_flow as get_mass_flow_cls
from .get_heat_transfer import get_heat_transfer as get_heat_transfer_cls
from .get_heat_transfer_sensible import get_heat_transfer_sensible as get_heat_transfer_sensible_cls
from .get_radiation_heat_transfer import get_radiation_heat_transfer as get_radiation_heat_transfer_cls
from .get_film_mass_flow import get_film_mass_flow as get_film_mass_flow_cls
from .get_film_heat_transfer import get_film_heat_transfer as get_film_heat_transfer_cls
from .get_electric_current import get_electric_current as get_electric_current_cls
from .get_pressure_work import get_pressure_work as get_pressure_work_cls
from .get_viscous_work import get_viscous_work as get_viscous_work_cls

class fluxes(Group):
    fluent_name = ...
    command_names = ...

    def mass_flow(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass flow rate at inlets and outlets.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def heat_transfer(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def heat_transfer_sensible(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sensible heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def radiation_heat_transfer(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print radiation heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def film_mass_flow(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print film mass flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def film_heat_transfer(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print film heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def electric_current(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print electric current rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def pressure_work(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print pressure work rate at moving boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def viscous_work(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print viscous work rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    query_names = ...

    def get_mass_flow(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print mass flow rate at inlets and outlets.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_heat_transfer(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_heat_transfer_sensible(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print sensible heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_radiation_heat_transfer(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print radiation heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_film_mass_flow(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print film mass flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_film_heat_transfer(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print film heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_electric_current(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print electric current rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_pressure_work(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print pressure work rate at moving boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

    def get_viscous_work(self, domain: str, zones: List[str], physics: List[str]):
        """
        Print viscous work rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : List
                Select zone name.
            physics : List
                Select the physics location.
        
        """

