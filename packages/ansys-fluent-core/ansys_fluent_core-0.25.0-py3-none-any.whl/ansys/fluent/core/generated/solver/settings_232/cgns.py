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
from .scope import scope as scope_cls
from .cell_zones import cell_zones as cell_zones_cls
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .format_class import format_class as format_class_cls
from .cgns_scalar import cgns_scalar as cgns_scalar_cls

class cgns(Command):
    """
    Write a CGNS file.
    
    Parameters
    ----------
        name : str
            'name' child.
        scope : str
            'scope' child.
        cell_zones : List
            'cell_zones' child.
        surfaces : List
            'surfaces' child.
        cell_centered : bool
            'cell_centered' child.
        format_class : str
            'format_class' child.
        cgns_scalar : List
            'cgns_scalar' child.
    
    """

    fluent_name = "cgns"

    argument_names = \
        ['name', 'scope', 'cell_zones', 'surfaces', 'cell_centered',
         'format_class', 'cgns_scalar']

    _child_classes = dict(
        name=name_cls,
        scope=scope_cls,
        cell_zones=cell_zones_cls,
        surfaces=surfaces_cls,
        cell_centered=cell_centered_cls,
        format_class=format_class_cls,
        cgns_scalar=cgns_scalar_cls,
    )

    return_type = "<object object at 0x7f641facffd0>"
