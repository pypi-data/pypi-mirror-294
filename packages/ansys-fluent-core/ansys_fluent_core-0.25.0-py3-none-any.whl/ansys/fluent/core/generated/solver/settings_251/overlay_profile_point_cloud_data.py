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

from .overlay import overlay as overlay_cls
from .profile_name_1 import profile_name as profile_name_cls
from .graphics_object import graphics_object as graphics_object_cls
from .display_contour import display_contour as display_contour_cls
from .field_variable import field_variable as field_variable_cls

class overlay_profile_point_cloud_data(Command):
    """
    Overlay Display Profile Point cloud data Command.
    
    Parameters
    ----------
        overlay : bool
            Overlay profile point cloud data.
        profile_name : str
            Profile name.
        graphics_object : str
            Graphics Object.
        display_contour : bool
            Enable/Disable Profile Field Contour.
        field_variable : str
            Field variable.
    
    """

    fluent_name = "overlay-profile-point-cloud-data"

    argument_names = \
        ['overlay', 'profile_name', 'graphics_object', 'display_contour',
         'field_variable']

    _child_classes = dict(
        overlay=overlay_cls,
        profile_name=profile_name_cls,
        graphics_object=graphics_object_cls,
        display_contour=display_contour_cls,
        field_variable=field_variable_cls,
    )

