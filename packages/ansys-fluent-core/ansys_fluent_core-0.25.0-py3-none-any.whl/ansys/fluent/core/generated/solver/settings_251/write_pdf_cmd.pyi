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

from .binary import binary as binary_cls
from .write_pdf_file import write_pdf_file as write_pdf_file_cls

class write_pdf_cmd(Command):
    fluent_name = ...
    argument_names = ...
    binary: binary_cls = ...
    write_pdf_file: write_pdf_file_cls = ...
