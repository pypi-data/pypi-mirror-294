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

from .table_parameters import table_parameters as table_parameters_cls
from .calc_pdf import calc_pdf as calc_pdf_cls
from .write_pdf_cmd import write_pdf_cmd as write_pdf_cmd_cls

class table(Group):
    """
    PDF Table Options.
    """

    fluent_name = "table"

    child_names = \
        ['table_parameters']

    command_names = \
        ['calc_pdf', 'write_pdf_cmd']

    _child_classes = dict(
        table_parameters=table_parameters_cls,
        calc_pdf=calc_pdf_cls,
        write_pdf_cmd=write_pdf_cmd_cls,
    )

