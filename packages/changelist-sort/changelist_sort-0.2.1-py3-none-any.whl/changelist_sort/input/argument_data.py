"""The Arguments Received from the Command Line Input.

This DataClass is created after the argument syntax is validated.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """
    The syntactically valid arguments recevied by the Program.

    Fields:
    - workspace_path (str): The path to the workspace file.
    - developer_sort (bool): Flag for the Developer SortMode.
    - sourceset_sort (bool): Flag for the SourceSet SortMode.
    - remove_empty (bool): Flag indicating that empty changelists should be removed.
    """
    workspace_path: str | None
    developer_sort: bool = False
    sourceset_sort: bool = False
    remove_empty: bool = False
