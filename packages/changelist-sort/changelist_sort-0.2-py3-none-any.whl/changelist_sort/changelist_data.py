"""The Data Class for a ChangeList.
"""
from dataclasses import dataclass, field

from changelist_sort import list_key
from changelist_sort.change_data import ChangeData
from changelist_sort.list_key import ListKey


@dataclass(frozen=True)
class ChangelistData:
    """
    The complete Data class representing a ChangeList.
    
    Properties:
    - id (str): The unique id of the changelist.
    - name (str): The name of the changelist.
    - changes (list[ChangeData]): The list of file changes in the changelist.
    - comment (str): The comment associated with the changelist.
    - is_default (bool): Whether this is the active changelist.

    Post Init Properties:
    - simple_name (str): A simplified string derived from the name property.
    """
    id: str
    name: str
    changes: list[ChangeData] = field(default_factory=lambda: [])
    comment: str = ""
    is_default: bool = False
    
    list_key: ListKey = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'list_key', list_key.compute_key(self.name))
