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

from .timestep_selector import timestep_selector as timestep_selector_cls
from .enable_22 import enable as enable_cls
from .display_12 import display as display_cls
from .monitor_5 import monitor as monitor_cls
from .animation import animation as animation_cls
from .compare_results import compare_results as compare_results_cls
from .compute_and_clip_range_1 import compute_and_clip_range as compute_and_clip_range_cls

class transient_post_processing(Group):
    """
    Enter transient postprocessing menu.
    """

    fluent_name = "transient-post-processing"

    child_names = \
        ['timestep_selector']

    command_names = \
        ['enable', 'display', 'monitor', 'animation', 'compare_results',
         'compute_and_clip_range']

    _child_classes = dict(
        timestep_selector=timestep_selector_cls,
        enable=enable_cls,
        display=display_cls,
        monitor=monitor_cls,
        animation=animation_cls,
        compare_results=compare_results_cls,
        compute_and_clip_range=compute_and_clip_range_cls,
    )

