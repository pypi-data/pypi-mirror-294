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
    """
    PDF Chemistry Options.
    """

    fluent_name = "chemistry"

    child_names = \
        ['energy_treatment', 'state_relation', 'options', 'model_settings',
         'flamelet_options', 'file_type', 'flamelet_type',
         'flamelet_solution_method', 'premixed_model']

    command_names = \
        ['import_standard_flamelet', 'import_rif_flamelet']

    _child_classes = dict(
        energy_treatment=energy_treatment_cls,
        state_relation=state_relation_cls,
        options=options_cls,
        model_settings=model_settings_cls,
        flamelet_options=flamelet_options_cls,
        file_type=file_type_cls,
        flamelet_type=flamelet_type_cls,
        flamelet_solution_method=flamelet_solution_method_cls,
        premixed_model=premixed_model_cls,
        import_standard_flamelet=import_standard_flamelet_cls,
        import_rif_flamelet=import_rif_flamelet_cls,
    )

