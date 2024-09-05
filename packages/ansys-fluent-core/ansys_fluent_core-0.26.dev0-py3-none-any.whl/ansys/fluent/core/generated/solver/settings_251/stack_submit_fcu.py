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

from .submit import submit as submit_cls

class stack_submit_fcu(Command):
    """
    Apply stack units settings.
    
    Parameters
    ----------
        submit : bool
            Submit new stack setup.
    
    """

    fluent_name = "stack-submit-fcu"

    argument_names = \
        ['submit']

    _child_classes = dict(
        submit=submit_cls,
    )

