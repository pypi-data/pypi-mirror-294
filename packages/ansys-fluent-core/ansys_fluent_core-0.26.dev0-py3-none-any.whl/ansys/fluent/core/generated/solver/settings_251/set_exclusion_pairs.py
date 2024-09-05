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

from .exclude_pairs import exclude_pairs as exclude_pairs_cls
from .exclusion_pairs import exclusion_pairs as exclusion_pairs_cls

class set_exclusion_pairs(Command):
    """
    Set one-to-one interface exclusion pairs.
    
    Parameters
    ----------
        exclude_pairs : bool
            Excluding specified zone pairs.
        exclusion_pairs : List
            Select wall and/or interface zones for pairing. no input will clear the exclusion paris.
    
    """

    fluent_name = "set-exclusion-pairs"

    argument_names = \
        ['exclude_pairs', 'exclusion_pairs']

    _child_classes = dict(
        exclude_pairs=exclude_pairs_cls,
        exclusion_pairs=exclusion_pairs_cls,
    )

