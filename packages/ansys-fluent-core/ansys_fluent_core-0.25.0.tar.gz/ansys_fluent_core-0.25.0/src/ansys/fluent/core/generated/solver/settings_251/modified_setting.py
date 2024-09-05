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

from .setting_type import setting_type as setting_type_cls

class modified_setting(Command):
    """
    Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.
    
    Parameters
    ----------
        setting_type : List
            'setting_type' child.
    
    """

    fluent_name = "modified-setting"

    argument_names = \
        ['setting_type']

    _child_classes = dict(
        setting_type=setting_type_cls,
    )

