"""Valid Input Data Class.
"""
from dataclasses import dataclass
from pathlib import Path

from changelist_sort.sorting.sort_mode import SortMode


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

    Fields:
    - workspace_xml (str): The contents of the Workspace XML file.
    - workspace_path (Path): The Path to the Workspace File.
    - sort_mode (SortMode): The selected Sorting Mode enum value.
    - remove_empty (bool): Whether to remove empty changelists after sort.
    """
    workspace_xml: str
    workspace_path: Path
    sort_mode: SortMode = SortMode.MODULE
    remove_empty: bool = False
