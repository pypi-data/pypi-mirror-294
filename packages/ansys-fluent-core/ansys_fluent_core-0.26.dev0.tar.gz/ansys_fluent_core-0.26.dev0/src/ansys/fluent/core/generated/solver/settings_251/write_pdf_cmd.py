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

from .binary import binary as binary_cls
from .write_pdf_file import write_pdf_file as write_pdf_file_cls

class write_pdf_cmd(Command):
    """
    Write a PDF file.
    
    Parameters
    ----------
        binary : bool
            Write in binary format.
        write_pdf_file : str
            Name PDF File.
    
    """

    fluent_name = "write-pdf-cmd"

    argument_names = \
        ['binary', 'write_pdf_file']

    _child_classes = dict(
        binary=binary_cls,
        write_pdf_file=write_pdf_file_cls,
    )

