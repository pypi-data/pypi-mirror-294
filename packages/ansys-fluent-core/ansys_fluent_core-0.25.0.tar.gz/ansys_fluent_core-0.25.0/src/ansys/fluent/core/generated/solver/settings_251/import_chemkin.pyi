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

from .kinetics_input_file import kinetics_input_file as kinetics_input_file_cls
from .thermodb_input_file import thermodb_input_file as thermodb_input_file_cls
from .surf_mech import surf_mech as surf_mech_cls
from .trans_prop import trans_prop as trans_prop_cls
from .trans_input_file import trans_input_file as trans_input_file_cls
from .surfchem_input_file import surfchem_input_file as surfchem_input_file_cls

class import_chemkin(Command):
    fluent_name = ...
    argument_names = ...
    kinetics_input_file: kinetics_input_file_cls = ...
    thermodb_input_file: thermodb_input_file_cls = ...
    surf_mech: surf_mech_cls = ...
    trans_prop: trans_prop_cls = ...
    trans_input_file: trans_input_file_cls = ...
    surfchem_input_file: surfchem_input_file_cls = ...
