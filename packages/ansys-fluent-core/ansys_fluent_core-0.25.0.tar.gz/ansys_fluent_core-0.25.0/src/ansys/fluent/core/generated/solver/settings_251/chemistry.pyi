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

from .energy_treatment import energy_treatment as energy_treatment_cls
from .state_relation import state_relation as state_relation_cls
from .options_3 import options as options_cls
from .model_settings import model_settings as model_settings_cls
from .flamelet_options import flamelet_options as flamelet_options_cls
from .file_type_2 import file_type as file_type_cls
from .flamelet_type import flamelet_type as flamelet_type_cls
from .flamelet_solution_method import flamelet_solution_method as flamelet_solution_method_cls
from .premixed_model import premixed_model as premixed_model_cls
from .import_standard_flamelet import import_standard_flamelet as import_standard_flamelet_cls
from .import_rif_flamelet import import_rif_flamelet as import_rif_flamelet_cls

class chemistry(Group):
    fluent_name = ...
    child_names = ...
    energy_treatment: energy_treatment_cls = ...
    state_relation: state_relation_cls = ...
    options: options_cls = ...
    model_settings: model_settings_cls = ...
    flamelet_options: flamelet_options_cls = ...
    file_type: file_type_cls = ...
    flamelet_type: flamelet_type_cls = ...
    flamelet_solution_method: flamelet_solution_method_cls = ...
    premixed_model: premixed_model_cls = ...
    command_names = ...

    def import_standard_flamelet(self, standard_flamelet_file: List[str]):
        """
        Import Standard Flamelet.
        
        Parameters
        ----------
            standard_flamelet_file : List
                Import Standard Flamelet File.
        
        """

    def import_rif_flamelet(self, rif_prp_file: str, rif_flamelet_file: str):
        """
        Import CFX-RIF Flamelet.
        
        Parameters
        ----------
            rif_prp_file : str
                Import CFX-RIF Property PRP File.
            rif_flamelet_file : str
                Import RIF Flamelet File.
        
        """

