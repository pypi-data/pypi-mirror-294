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

from .mf_1 import mf as mf_cls
from .urf import urf as urf_cls

class solution_controls(Command):
    """
    Specification of mapped frequency and under-relaxation factor for mapped interfaces.
    
    Parameters
    ----------
        mf : int
            'mf' child.
        urf : real
            'urf' child.
    
    """

    fluent_name = "solution-controls"

    argument_names = \
        ['mf', 'urf']

    _child_classes = dict(
        mf=mf_cls,
        urf=urf_cls,
    )

    return_type = "<object object at 0x7f641d76a000>"
