"""The Arguments Received from the Command Line Input.

This DataClass is created after the argument syntax is validated.

Syntax Validation:
-
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """
    The syntactically valid arguments recevied by the Program.

    Fields:
    - workspace_path (str): The path to the workspace file.
    - developer_sort (bool):
    - sourceset_sort (bool):
    """
    workspace_path: str | None
    developer_sort: bool = False
    sourceset_sort: bool = False
