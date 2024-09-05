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

from .data_file1 import data_file1 as data_file1_cls
from .data_file2 import data_file2 as data_file2_cls
from .compare import compare as compare_cls

class compare_results(Command):
    """
    Result comparison.
    
    Parameters
    ----------
        data_file1 : str
            Select first data file for result comparison.
        data_file2 : str
            Select second data file for result comparison.
        compare : str
            Select object for result comparison.
    
    """

    fluent_name = "compare-results"

    argument_names = \
        ['data_file1', 'data_file2', 'compare']

    _child_classes = dict(
        data_file1=data_file1_cls,
        data_file2=data_file2_cls,
        compare=compare_cls,
    )

