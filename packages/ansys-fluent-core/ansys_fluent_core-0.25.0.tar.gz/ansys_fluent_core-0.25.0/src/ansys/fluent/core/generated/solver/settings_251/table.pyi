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

from .table_parameters import table_parameters as table_parameters_cls
from .calc_pdf import calc_pdf as calc_pdf_cls
from .write_pdf_cmd import write_pdf_cmd as write_pdf_cmd_cls

class table(Group):
    fluent_name = ...
    child_names = ...
    table_parameters: table_parameters_cls = ...
    command_names = ...

    def calc_pdf(self, ):
        """
        Calculate PDF.
        """

    def write_pdf_cmd(self, binary: bool, write_pdf_file: str):
        """
        Write a PDF file.
        
        Parameters
        ----------
            binary : bool
                Write in binary format.
            write_pdf_file : str
                Name PDF File.
        
        """

