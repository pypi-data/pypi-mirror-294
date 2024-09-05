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

from .create_1 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .detect_surfaces import detect_surfaces as detect_surfaces_cls
from .clear_repeats import clear_repeats as clear_repeats_cls
from .periodic_instances_child import periodic_instances_child


class periodic_instances(NamedObject[periodic_instances_child], CreatableNamedObjectMixin[periodic_instances_child]):
    fluent_name = ...
    command_names = ...

    def create(self, name: str):
        """
        Create an instance of this.
        
        Parameters
        ----------
            name : str
                Set name for an object.
        
        """

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : List
                Select objects to be deleted.
        
        """

    def rename(self, new: str, old: str):
        """
        Rename the object.
        
        Parameters
        ----------
            new : str
                New name for the object.
            old : str
                Select object to rename.
        
        """

    def list(self, ):
        """
        List the names of the objects.
        """

    def list_properties(self, object_name: str):
        """
        List active properties of the object.
        
        Parameters
        ----------
            object_name : str
                Select object for which properties are to be listed.
        
        """

    def make_a_copy(self, from_: str, to: str):
        """
        Create a copy of the object.
        
        Parameters
        ----------
            from_ : str
                Select the object to duplicate.
            to : str
                Specify the name of the new object.
        
        """

    def detect_surfaces(self, clear_current_instances: bool):
        """
        Detect the surfaces for the periodic instance.
        
        Parameters
        ----------
            clear_current_instances : bool
                Clear the current periodic instances.
        
        """

    def clear_repeats(self, ):
        """
        Clear the periodic instance repeats.
        """

    child_object_type: periodic_instances_child = ...
