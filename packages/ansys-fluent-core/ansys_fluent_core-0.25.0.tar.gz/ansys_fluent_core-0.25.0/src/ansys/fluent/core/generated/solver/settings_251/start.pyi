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

from typing import Union, List, Tuple

from .session_name import session_name as session_name_cls
from .port import port as port_cls
from .port_span import port_span as port_span_cls
from .job_service_url import job_service_url as job_service_url_cls
from .email_id import email_id as email_id_cls

class start(Command):
    fluent_name = ...
    argument_names = ...
    session_name: session_name_cls = ...
    port: port_cls = ...
    port_span: port_span_cls = ...
    job_service_url: job_service_url_cls = ...
    email_id: email_id_cls = ...
