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

from .set_filetype import set_filetype as set_filetype_cls

class set_cgns_export_filetype(Command):
    """
    Select HDF5 or ADF as file format for CGNS.
    
    Parameters
    ----------
        set_filetype : bool
            'set_filetype' child.
    
    """

    fluent_name = "set-cgns-export-filetype"

    argument_names = \
        ['set_filetype']

    _child_classes = dict(
        set_filetype=set_filetype_cls,
    )

    return_type = "<object object at 0x7f641face770>"
