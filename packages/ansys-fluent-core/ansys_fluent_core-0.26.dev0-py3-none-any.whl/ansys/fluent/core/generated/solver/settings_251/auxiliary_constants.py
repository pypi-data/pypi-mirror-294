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

from .creal import creal as creal_cls
from .cnw_sub import cnw_sub as cnw_sub_cls
from .cjet_aux import cjet_aux as cjet_aux_cls
from .cbf_lam import cbf_lam as cbf_lam_cls
from .cbf_tur import cbf_tur as cbf_tur_cls

class auxiliary_constants(Group):
    """
    Auxiliary GEKO model constanst group.
    """

    fluent_name = "auxiliary-constants"

    child_names = \
        ['creal', 'cnw_sub', 'cjet_aux', 'cbf_lam', 'cbf_tur']

    _child_classes = dict(
        creal=creal_cls,
        cnw_sub=cnw_sub_cls,
        cjet_aux=cjet_aux_cls,
        cbf_lam=cbf_lam_cls,
        cbf_tur=cbf_tur_cls,
    )

