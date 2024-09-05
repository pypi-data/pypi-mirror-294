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

from .xyz import xyz as xyz_cls

class position(Command):
    """
    Set the camera position.
    
    Parameters
    ----------
        xyz : List
            'xyz' child.
    
    """

    fluent_name = "position"

    argument_names = \
        ['xyz']

    _child_classes = dict(
        xyz=xyz_cls,
    )

