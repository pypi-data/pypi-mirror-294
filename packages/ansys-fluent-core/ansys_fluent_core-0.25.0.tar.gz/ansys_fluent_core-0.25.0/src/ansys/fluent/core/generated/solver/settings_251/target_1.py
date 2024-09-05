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

class target(Command):
    """
    Set the point to be the center of the camera view.
    
    Parameters
    ----------
        xyz : List
            'xyz' child.
    
    """

    fluent_name = "target"

    argument_names = \
        ['xyz']

    _child_classes = dict(
        xyz=xyz_cls,
    )

