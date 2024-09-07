""" Developer Changelist Settings and Methods
"""
from dataclasses import dataclass

from changelist_sort.change_data import ChangeData
from changelist_sort.list_key import ListKey
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.workspace.developer_file_pattern import DeveloperFilePattern


@dataclass(frozen=True)
class DeveloperChangelist:
    """
    The Changelist Defined by the Developer.

    Parameters:
    - list_key (ListKey): The Key and Name of the Changelist.
    - module_type (ModuleType): The Type of Module to match Files with.
    - file_patterns (tuple[DeveloperFilePattern]): 
    """
    module_type: ModuleType | None
    list_key: ListKey
    file_patterns: tuple[DeveloperFilePattern]

    def check_file(self, file: ChangeData) -> bool:
        """
        Determine if the File can be added to this Changelist.

        Parameters:
        - file (ChangeData): The ChangeData of the File to pattern match.

        Returns:
        True if the File matches all patterns in this Changelist.
        """
        for fp in self.file_patterns:
            if not fp.check_file(file):
                return False
        return True
