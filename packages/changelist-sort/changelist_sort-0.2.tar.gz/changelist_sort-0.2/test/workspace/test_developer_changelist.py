""" Testing Developer Changelist
"""
from test import data_provider

from changelist_sort import list_key
from changelist_sort.sorting.developer_sort import _INPUT_PACKAGE_PATTERN, _SRC_DIR_PATTERN
from changelist_sort.workspace.developer_changelist import DeveloperChangelist


def get_dc_src_input() -> DeveloperChangelist:
    return DeveloperChangelist(
        None,
        list_key.compute_key('Input Source Package'),
        (
            _SRC_DIR_PATTERN,
            _INPUT_PACKAGE_PATTERN
        )
    )


def test_check_file_src_dir_input_pattern_input_data_returns_true():
    instance = get_dc_src_input()
    assert instance.check_file(data_provider.get_change_data('/changelist_sort/input/input_data.py'))
    

def test_check_file_src_dir_input_pattern_init_file_returns_false():
    instance = get_dc_src_input()
    assert not instance.check_file(data_provider.get_change_data('/changelist_sort/__init__.py'))
