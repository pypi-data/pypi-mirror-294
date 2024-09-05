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

from .design_points import design_points as design_points_cls

class clear_generated_data(Command):
    """
    Clear Generated Data.
    
    Parameters
    ----------
        design_points : List
            'design_points' child.
    
    """

    fluent_name = "clear-generated-data"

    argument_names = \
        ['design_points']

    _child_classes = dict(
        design_points=design_points_cls,
    )

