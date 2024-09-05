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


class exclusion_pairs(StringList, AllowedValuesMixin):
    """
    Select wall and/or interface zones for pairing. no input will clear the exclusion paris.
    """

    fluent_name = "exclusion-pairs"

