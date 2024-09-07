""" Testing Module Sort Methods.
"""
import pytest

from test import data_provider
from changelist_sort.sorting import file_sort
from changelist_sort.sorting import module_sort
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting.module_sort import sort_file_by_module, is_sorted_by_module


@pytest.mark.parametrize(
    'key', [ModuleType.MODULE, ModuleType.HIDDEN]
)
def test_get_module_keys_user_modules(key):
    result = module_sort.get_module_keys(key)
    assert result == tuple()


def test_sort_file_by_module_empty_map_empty_file_returns_false():
    cl_map = ChangelistMap()
    empty_file = ChangeData()
    assert not sort_file_by_module(cl_map, empty_file)


def test_sort_file_by_module_empty_map_module_src_file_returns_true():
    cl_map = ChangelistMap()
    src_file = data_provider.get_change_data(
        data_provider.MODULE_SRC_PATH,
    )
    assert sort_file_by_module(cl_map, src_file)
    # Check CL Map for new Changelist
    new_cl = cl_map.search('module')
    assert new_cl is not None
    assert new_cl.name == 'Module'


def test_sort_file_by_module_app_gradle_file_returns_true_inserts_build_updates():
    cl_map = ChangelistMap()
    test_file = data_provider.get_app_gradle_build_change_data()
    assert sort_file_by_module(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_file_by_module_gradle_properties_returns_true_inserts_build_updates():
    cl_map = ChangelistMap()
    test_file = data_provider.get_app_gradle_build_change_data()
    assert sort_file_by_module(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_file_by_module_github_workflows_returns_true_inserts_github():
    cl_map = ChangelistMap()
    test_file = data_provider.get_github_workflows_change_data()
    assert sort_file_by_module(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Github'


def test_sort_file_by_module_empty_file_returns_false():
    cl_map = ChangelistMap()
    empty_file = ChangeData()
    assert not sort_file_by_module(cl_map, empty_file)


def test_sort_file_by_module_app_cl_app_gradle_returns_true():
    cl_map = ChangelistMap()
    cl_map.insert(data_provider.get_app_changelist())
    new_cd = data_provider.get_app_gradle_build_change_data()
    assert sort_file_by_module(cl_map, new_cd)
    # A new Changelist is created called Build Updates
    result = cl_map.get_lists()
    assert len(result) == 2
    cl_0 = result[0]
    assert cl_0.name == 'App'
    cl_1 = result[1]
    assert cl_1.name == 'Build Updates'
    assert new_cd in cl_1.changes


def test_sort_file_by_module_build_updates_cl_app_gradle_returns_true():
    cl_map = ChangelistMap()
    cl_map.insert(data_provider.get_build_updates_changelist())
    new_cd = data_provider.get_app_gradle_build_change_data()
    assert sort_file_by_module(cl_map, new_cd)
    # The Build Updates Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    assert result[0].name == 'Build Updates'


def test_sort_file_by_module_root_cl_readme_returns_true():
    cl_map = ChangelistMap()
    cl_map.insert(data_provider.get_root_changelist())
    new_cd = data_provider.get_root_readme_change_data()
    assert sort_file_by_module(cl_map, new_cd)
    # The Build Updates Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    assert result[0].name == 'Root'
    assert len(result[0].changes) == 1


def test_sort_file_by_module_module_cl_module_src_returns_true():
    cl_map = ChangelistMap()
    cl_map.insert(data_provider.get_module_changelist())
    new_cd = data_provider.get_module_src_change_data()
    assert sort_file_by_module(cl_map, new_cd)
    # The Src file is added to the existing changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    cl_0 = result[0]
    assert cl_0.name == 'Module'
    assert new_cd in cl_0.changes


def test_sort_file_by_module_zero_len_module_returns_false():
    new_cd = data_provider.get_change_data('//hello.py')
    assert not sort_file_by_module(None, new_cd)


def test_sort_file_by_module_root_readme_returns_true():
    cl_map = ChangelistMap()
    new_cd = data_provider.get_root_readme_change_data()
    assert file_sort.get_module_type(new_cd) == ModuleType.ROOT
    assert sort_file_by_module(cl_map, new_cd)


def test_is_sorted_by_module_module_cl():
    cl = data_provider.get_module_changelist()
    for file in cl.changes:
        assert is_sorted_by_module(cl.list_key, file)


def test_is_sorted_by_module_app_cl_app_gradle_returns_false():
    cl = data_provider.get_app_changelist()
    assert not is_sorted_by_module(
        cl.list_key, data_provider.get_app_gradle_build_change_data()
    )


def test_is_sorted_by_module_app_cl_strings_res_returns_true():
    cl = data_provider.get_app_changelist()
    assert is_sorted_by_module(
        cl.list_key, data_provider.get_change_data('/app/src/main/res/values/strings.xml')
    )


def test_is_sorted_by_module_app_cl_src_file_returns_true():
    cl = data_provider.get_app_changelist()
    assert is_sorted_by_module(
        cl.list_key, data_provider.get_change_data('/app/src/main/java/app/Main.java')
    )


def test_is_sorted_by_module_build_updates_cl_returns_true():
    cl = data_provider.get_build_updates_changelist()
    for file in cl.changes:
        assert is_sorted_by_module(cl.list_key, file)


def test_is_sorted_by_module_build_updates_cl_gradle_properties_returns_true():
    cl = data_provider.get_build_updates_changelist()
    assert is_sorted_by_module(
        cl.list_key, data_provider.get_gradle_properties_change_data()
    )


def test_is_sorted_by_module_github_cl():
    cl = data_provider.get_github_changelist()
    assert is_sorted_by_module(
        cl.list_key, data_provider.get_change_data('/.github/workflow/test.yml')
    )


def test_is_sorted_by_module_github_cl_dependabot_returns_true():
    cl = data_provider.get_github_changelist()
    assert is_sorted_by_module(
        cl.list_key, data_provider.get_change_data('/.github/dependabot.yml')
    )
