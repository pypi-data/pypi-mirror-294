""" Testing Workspace Package Init Module Methods.
"""

from changelist_sort.input.input_data import InputData
from changelist_sort.workspace import get_workspace_tree


def test_get_workspace_tree_empty_str_raises_exit():
    test_input = InputData(
        workspace_xml='',
        workspace_path=None,
    )
    try:
        get_workspace_tree(test_input)
        assert False
    except SystemExit:
        assert True
