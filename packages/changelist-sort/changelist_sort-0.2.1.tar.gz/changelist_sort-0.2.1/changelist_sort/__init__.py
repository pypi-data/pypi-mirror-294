""" Main Package Methods.
"""
from changelist_sort import workspace
from changelist_sort.sorting import sort
from changelist_sort.input.input_data import InputData


def sort_changelists(
    input_data: InputData,
):
    """
    Sort the given Changelists and write them to the Workspace File.
    """
    ws_tree = workspace.get_workspace_tree(input_data)
    sorted_lists = sort(
        ws_tree.extract_list_elements(),
        input_data.sort_mode
    )
    if input_data.remove_empty:
        sorted_lists = list(filter(
            lambda x: len(x.changes) > 0, sorted_lists
        ))
    ws_tree.replace_changelists(sorted_lists)
    workspace.write_workspace_tree(
        ws_tree, input_data.workspace_path
    )
