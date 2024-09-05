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

from typing import Union, List, Tuple

from .timestep_selector import timestep_selector as timestep_selector_cls
from .enable_22 import enable as enable_cls
from .display_12 import display as display_cls
from .monitor_5 import monitor as monitor_cls
from .animation import animation as animation_cls
from .compare_results import compare_results as compare_results_cls
from .compute_and_clip_range_1 import compute_and_clip_range as compute_and_clip_range_cls

class transient_post_processing(Group):
    fluent_name = ...
    child_names = ...
    timestep_selector: timestep_selector_cls = ...
    command_names = ...

    def enable(self, enabled: bool):
        """
        Enable/Disable transient postprocessing?.
        
        Parameters
        ----------
            enabled : bool
                Enable/Disable transient postprocessing?.
        
        """

    def display(self, display: List[str]):
        """
        Transient display.
        
        Parameters
        ----------
            display : List
                Select graphics object name(s) for transient display.
        
        """

    def monitor(self, monitor: List[str]):
        """
        Transient monitor.
        
        Parameters
        ----------
            monitor : List
                Select report file name(s) for transient monitor.
        
        """

    def animation(self, animate: List[str]):
        """
        Create transient animation(s).
        
        Parameters
        ----------
            animate : List
                Select animation object name(s) for transient animation.
        
        """

    def compare_results(self, data_file1: str, data_file2: str, compare: str):
        """
        Result comparison.
        
        Parameters
        ----------
            data_file1 : str
                Select first data file for result comparison.
            data_file2 : str
                Select second data file for result comparison.
            compare : str
                Select object for result comparison.
        
        """

    def compute_and_clip_range(self, compute_and_clip_range: str):
        """
        Compute and clip range for transient post processing.
        
        Parameters
        ----------
            compute_and_clip_range : str
                Select graphics object name to compute and clip range for transient post processing.
        
        """

