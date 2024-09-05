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

from .report_name import report_name as report_name_cls
from .file_name_path import file_name_path as file_name_path_cls

class export_simulation_report_as_pdf(Command):
    """
    Export the provided simulation report as a PDF file.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        file_name_path : str
            'file_name_path' child.
    
    """

    fluent_name = "export-simulation-report-as-pdf"

    argument_names = \
        ['report_name', 'file_name_path']

    _child_classes = dict(
        report_name=report_name_cls,
        file_name_path=file_name_path_cls,
    )

    return_type = "<object object at 0x7f115b5a37e0>"
