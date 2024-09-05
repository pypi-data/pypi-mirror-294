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

from .compute_and_clip_range import compute_and_clip_range as compute_and_clip_range_cls

class compute_and_clip_range(Command):
    """
    Compute and clip range for transient post processing.
    
    Parameters
    ----------
        compute_and_clip_range : str
            Select graphics object name to compute and clip range for transient post processing.
    
    """

    fluent_name = "compute-and-clip-range"

    argument_names = \
        ['compute_and_clip_range']

    _child_classes = dict(
        compute_and_clip_range=compute_and_clip_range_cls,
    )

