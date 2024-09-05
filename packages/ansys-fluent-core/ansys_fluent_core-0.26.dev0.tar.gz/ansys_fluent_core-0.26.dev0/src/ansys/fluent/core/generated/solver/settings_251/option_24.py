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


class option(String, AllowedValuesMixin):
    """
    (0) basic:           name-prefix:##
    (1) name-based:      name-prefix:##:interface_name1::interface_name2
    (2) ID-based:        name-prefix:##:interface_ID1::interface-ID2
    (3) adjacency-based: name-prefix:##:cell_zone_name1::cell_zone_name2.
    """

    fluent_name = "option"

