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

from .oil_flow_1 import oil_flow as oil_flow_cls
from .onzone import onzone as onzone_cls
from .reverse_1 import reverse as reverse_cls
from .node_values_2 import node_values as node_values_cls
from .accuracy_controls import accuracy_controls as accuracy_controls_cls
from .step_size_1 import step_size as step_size_cls
from .tolerance_4 import tolerance as tolerance_cls
from .relative_2 import relative as relative_cls
from .step import step as step_cls
from .skip_1 import skip as skip_cls
from .coarsen_1 import coarsen as coarsen_cls

class option(Group):
    """
    Check the control options.
    """

    fluent_name = "option"

    child_names = \
        ['oil_flow', 'onzone', 'reverse', 'node_values', 'accuracy_controls',
         'step_size', 'tolerance', 'relative', 'step', 'skip', 'coarsen']

    _child_classes = dict(
        oil_flow=oil_flow_cls,
        onzone=onzone_cls,
        reverse=reverse_cls,
        node_values=node_values_cls,
        accuracy_controls=accuracy_controls_cls,
        step_size=step_size_cls,
        tolerance=tolerance_cls,
        relative=relative_cls,
        step=step_cls,
        skip=skip_cls,
        coarsen=coarsen_cls,
    )

