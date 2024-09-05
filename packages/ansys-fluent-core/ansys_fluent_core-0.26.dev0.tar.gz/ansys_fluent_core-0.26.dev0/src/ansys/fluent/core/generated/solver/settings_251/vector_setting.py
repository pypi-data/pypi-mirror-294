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

from .style_1 import style as style_cls
from .vector_of_1 import vector_of as vector_of_cls
from .variable_length_1 import variable_length as variable_length_cls
from .vector_length_1 import vector_length as vector_length_cls
from .constant_length_1 import constant_length as constant_length_cls
from .scale_5 import scale as scale_cls
from .length_to_head_ratio_1 import length_to_head_ratio as length_to_head_ratio_cls
from .constant_color_1 import constant_color as constant_color_cls
from .color_6 import color as color_cls

class vector_setting(Group):
    """
    Particle-tracks Vector Style Settings.
    """

    fluent_name = "vector-setting"

    child_names = \
        ['style', 'vector_of', 'variable_length', 'vector_length',
         'constant_length', 'scale', 'length_to_head_ratio', 'constant_color',
         'color']

    _child_classes = dict(
        style=style_cls,
        vector_of=vector_of_cls,
        variable_length=variable_length_cls,
        vector_length=vector_length_cls,
        constant_length=constant_length_cls,
        scale=scale_cls,
        length_to_head_ratio=length_to_head_ratio_cls,
        constant_color=constant_color_cls,
        color=color_cls,
    )

