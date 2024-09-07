""" Sorting Package.
"""
from typing import Callable

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting.sort_mode import SortMode
from changelist_sort.sorting import developer_sort, module_sort, source_set_sort
from changelist_sort.sorting.list_sort import split_changelist


def sort(
    initial_list: list[ChangelistData],
    sort_mode: SortMode,
) -> list[ChangelistData]:
    """
    Processes InputData.

    Parameters:
    - initial_list (list[ChangelistData]): The list of Changelists to be sorted.
    - sort_mode (SortMode): The SortMode determining which sort rules to apply.

    Returns:
    str - The desired output.
    """
    unsorted_files = []
    cl_map = ChangelistMap()
    for cl in initial_list:
        if not cl_map.insert(cl):
            _handle_map_insertion_error()
        # Split CL based on SortMode criteria
        unsorted_files.extend(
            split_changelist(cl, _get_is_sorted_callable(sort_mode))
        )
    # This Callable depends on SortMode.
    #  It determines map keys, and executes map insertions.
    sort_result_string = _process_file_sort_results(list(map(
        _create_sorting_callable(cl_map, sort_mode),
        unsorted_files
    )))
    print(sort_result_string)
    return cl_map.get_lists()


def _create_sorting_callable(
    changelist_map: ChangelistMap,
    sort_mode: SortMode,
) -> Callable[[ChangeData], bool]:
    """
    Create a Callable that sorts ChangeData passed to it.
    """
    if sort_mode == SortMode.MODULE:
        return lambda x: module_sort.sort_file_by_module(changelist_map, x)
    if sort_mode == SortMode.DEVELOPER:
        return lambda x: developer_sort.sort_file_by_developer(changelist_map, x)
    if sort_mode == SortMode.SOURCESET:
        return lambda x: source_set_sort.sort_by_source_set(changelist_map, x)
    else:
        exit("SortMode not Implemented")


def _get_is_sorted_callable(
    sort_mode: SortMode
) -> Callable[[ListKey, ChangeData], bool]:
    """
    Obtain a Callable that determines whether a ChangeData is sorted.
    """
    if sort_mode == SortMode.MODULE:
        return module_sort.is_sorted_by_module
    if sort_mode == SortMode.DEVELOPER:
        return developer_sort.is_sorted_by_developer
    if sort_mode == SortMode.SOURCESET:
        return source_set_sort.is_sorted_by_source_set
    else:
        exit("SortMode not Implemented")


def _handle_map_insertion_error(
    cl_map: ChangelistMap,
    failure_cl: ChangelistData,
):
    """
    Using the given parameters, produce an error message and exit.

    Raises:
    SystemExit - containing error information.
    """
    if (existing_cl := cl_map.search(failure_cl.simple_name)) is not None:
        exit(f"Failed to Insert Changelist(name={failure_cl.name}) due to simplename key conflict with Changelist(name={existing_cl.name}).")
    elif cl_map.contains_id(failure_cl.id):
        exit(f"Failed to Insert Changelist(name={failure_cl.name}) due to id conflict (id={failure_cl.id}).")
    else:
        exit(f"Failed to Insert Changelist(name={failure_cl.name}) for unknown reason (neither key nor id conflict has occurred).")


def _process_file_sort_results(results: list[bool]) -> str:
    """
    Process and Format a string to print.
    """
    correct = sum(results)
    total = len(results)
    return f"Sorted {correct} of {total} unsorted files."
