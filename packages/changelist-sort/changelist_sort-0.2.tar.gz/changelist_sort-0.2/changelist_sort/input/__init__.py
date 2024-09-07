"""The Input Package for Changelist Sort
"""
from pathlib import Path

from changelist_sort.input.argument_data import ArgumentData
from changelist_sort.input.argument_parser import parse_arguments
from changelist_sort.input.file_validation import validate_input_file
from changelist_sort.input.input_data import InputData
from changelist_sort.sorting.sort_mode import SortMode


def validate_input(args_list: list[str]) -> InputData:
    """
    Validate the arguments and gather program input into InputData object.
    - Parses command line strings into ArgumentData object.
    - Finds Workspace file and reads it to a string.

    Returns:
    InputData - container for the program input.
    """
    arg_data = parse_arguments(args_list)
    ws_path = _find_workspace_file(arg_data)

    return InputData(
        workspace_xml=validate_input_file(ws_path),
        workspace_path=ws_path,
        sort_mode=_determine_sort_mode(arg_data),
    )


def _find_workspace_file(arg_data: ArgumentData) -> Path:
    """
    Generate a Path to the Workspace File.
    - If Path is given by CLI arguments, use it.
    - Otherwise, assume current directory is project root.

    Returns:
    Path - A Path object. Note, the actual file may not exist.
    """
    if arg_data.workspace_path is None:
        return Path('.') / '.idea' / 'workspace.xml'
    return Path(arg_data.workspace_path)


def _determine_sort_mode(arg_data: ArgumentData) -> SortMode:
    """
    Check the Argument Data flags to determine which SortMode to use.
    """
    if arg_data.developer_sort:
        return SortMode.DEVELOPER
    if arg_data.sourceset_sort:
        return SortMode.SOURCESET
    return SortMode.MODULE
