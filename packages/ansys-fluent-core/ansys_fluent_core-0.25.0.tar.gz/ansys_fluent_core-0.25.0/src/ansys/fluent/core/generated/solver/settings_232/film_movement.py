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

from .condensing_film import condensing_film as condensing_film_cls
from .all_film import all_film as all_film_cls

class film_movement(Group):
    """
    Set options for controlling the film particles movement.
    """

    fluent_name = "film-movement"

    child_names = \
        ['condensing_film', 'all_film']

    _child_classes = dict(
        condensing_film=condensing_film_cls,
        all_film=all_film_cls,
    )

    return_type = "<object object at 0x7f63fefe15d0>"
