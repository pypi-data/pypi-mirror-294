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

from .smoothing_1 import smoothing as smoothing_cls
from .remeshing import remeshing as remeshing_cls
from .layering import layering as layering_cls

class methods(Group):
    """
    'methods' child.
    """

    fluent_name = "methods"

    child_names = \
        ['smoothing', 'remeshing', 'layering']

    _child_classes = dict(
        smoothing=smoothing_cls,
        remeshing=remeshing_cls,
        layering=layering_cls,
    )

