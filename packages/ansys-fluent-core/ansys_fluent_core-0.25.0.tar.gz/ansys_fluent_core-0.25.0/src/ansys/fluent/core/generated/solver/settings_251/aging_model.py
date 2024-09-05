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

from .aging_model_enabled import aging_model_enabled as aging_model_enabled_cls
from .li_plating_enabled import li_plating_enabled as li_plating_enabled_cls
from .cathode_film_growth_enabled import cathode_film_growth_enabled as cathode_film_growth_enabled_cls
from .sei_growth import sei_growth as sei_growth_cls
from .li_plating import li_plating as li_plating_cls
from .cathode_film_growth import cathode_film_growth as cathode_film_growth_cls

class aging_model(Group):
    """
    Set up physics-based aging model.
    """

    fluent_name = "aging-model"

    child_names = \
        ['aging_model_enabled', 'li_plating_enabled',
         'cathode_film_growth_enabled', 'sei_growth', 'li_plating',
         'cathode_film_growth']

    _child_classes = dict(
        aging_model_enabled=aging_model_enabled_cls,
        li_plating_enabled=li_plating_enabled_cls,
        cathode_film_growth_enabled=cathode_film_growth_enabled_cls,
        sei_growth=sei_growth_cls,
        li_plating=li_plating_cls,
        cathode_film_growth=cathode_film_growth_cls,
    )

