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

from .name import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .techplot_scalars import techplot_scalars as techplot_scalars_cls

class dx(Command):
    """
    Write an IBM Data Explorer format file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surfaces : List
            'surfaces' child.
        techplot_scalars : List
            'techplot_scalars' child.
    
    """

    fluent_name = "dx"

    argument_names = \
        ['name', 'surfaces', 'techplot_scalars']

    _child_classes = dict(
        name=name_cls,
        surfaces=surfaces_cls,
        techplot_scalars=techplot_scalars_cls,
    )

    return_type = "<object object at 0x7f641facff60>"
