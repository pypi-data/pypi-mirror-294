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

from .enabled_53 import enabled as enabled_cls
from .field_7 import field as field_cls
from .option_37 import option as option_cls
from .minimum_3 import minimum as minimum_cls
from .maximum_3 import maximum as maximum_cls
from .filter_minimum_1 import filter_minimum as filter_minimum_cls
from .filter_maximum_1 import filter_maximum as filter_maximum_cls

class filter_setting(Group):
    """
    Specifies Particle Tracks Filter Settings.
    """

    fluent_name = "filter-setting"

    child_names = \
        ['enabled', 'field', 'option', 'minimum', 'maximum', 'filter_minimum',
         'filter_maximum']

    _child_classes = dict(
        enabled=enabled_cls,
        field=field_cls,
        option=option_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
        filter_minimum=filter_minimum_cls,
        filter_maximum=filter_maximum_cls,
    )

