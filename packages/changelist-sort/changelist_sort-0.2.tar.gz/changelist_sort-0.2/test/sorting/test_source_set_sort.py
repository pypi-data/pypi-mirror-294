""" Testing Source Set Sorting Methods.
"""
from changelist_sort import list_key
from changelist_sort.changelist_data import ChangelistData
from test import data_provider
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting.source_set_sort import _get_source_set_name, is_sorted_by_source_set, sort_by_source_set


_TEST_FIXTURES_CHANGE_PATH = '/module/src/testFixtures/java/module/MainTestFixture.java'
_ANDROID_TEST_CHANGE_PATH = '/module/src/androidTest/java/module/MainAndroidTest.java'


def test_sort_by_source_set_empty_map_empty_file_returns_false():
    cl_map = ChangelistMap()
    empty_file = ChangeData()
    assert not sort_by_source_set(cl_map, empty_file)
    

def test_sort_by_source_set_empty_map_module_src_file_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_module_src_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check the CL Name
    new_cl = cl_map.search('modulemain')
    assert new_cl is not None
    assert new_cl.name == 'Module Main'


def test_sort_by_source_set_empty_map_module_test_file_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_module_test_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check the CL Name
    new_cl = cl_map.search('moduletest')
    assert new_cl is not None
    assert new_cl.name == 'Module Test'


def test_sort_by_source_set_empty_map_module_debug_file_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_module_debug_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check the CL Name
    new_cl = cl_map.search('moduledebug')
    assert new_cl is not None
    assert new_cl.name == 'Module Debug'


def test_sort_by_source_set_empty_map_module_testfixtures_file_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_change_data(_TEST_FIXTURES_CHANGE_PATH)
    assert sort_by_source_set(cl_map, test_file)
    # Check the CL Name
    new_cl = cl_map.search('moduletestfixtures')
    assert new_cl is not None
    assert new_cl.name == 'Module Test Fixtures'


def test_sort_by_source_set_empty_map_module_androidtest_file_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_change_data(_ANDROID_TEST_CHANGE_PATH)
    assert sort_by_source_set(cl_map, test_file)
    # Check the CL Name
    new_cl = cl_map.search('moduleandroidtest')
    assert new_cl is not None
    assert new_cl.name == 'Module Android Test'


def test_sort_by_source_set_app_gradle_file_returns_true_inserts_build_updates():
    cl_map = ChangelistMap()
    test_file = data_provider.get_app_gradle_build_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_by_source_set_github_workflows_returns_true_inserts_github():
    cl_map = ChangelistMap()
    test_file = data_provider.get_github_workflows_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Github'


def test_sort_by_source_set_existing_module_cl_module_file_returns_true_inserts_module_main_cl():
    cl_map = ChangelistMap()
    # The Existing Module does not specify the Main source set
    assert cl_map.insert(data_provider.get_module_changelist([]))
    test_file = data_provider.get_module_src_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check CL Map for new ModuleMain Changelist and File
    result = cl_map.get_lists()
    assert len(result) == 2
    existing_module_cl = result[0]
    assert len(existing_module_cl.changes) == 0
    assert existing_module_cl.name == 'Module'
    new_main_cl = result[1]
    assert len(new_main_cl.changes) == 1
    assert new_main_cl.name == 'Module Main'


def test_sort_by_source_set_existing_module_cl_test_file_returns_true():
    cl_map = ChangelistMap()
    assert cl_map.insert(data_provider.get_module_changelist([]))
    test_file = data_provider.get_module_test_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check CL Map for Changelist and File
    result = cl_map.get_lists()
    assert len(result) == 2
    existing_module_cl = result[0]
    assert len(existing_module_cl.changes) == 0
    assert existing_module_cl.name == 'Module'
    new_test_cl = result[1]
    assert len(new_test_cl.changes) == 1
    assert new_test_cl.name == 'Module Test'


def test_sort_by_source_set_existing_moduletest_cl_moduletest_file_returns_true():
    cl_map = ChangelistMap()
    existing_test_cl = ChangelistData(
        id='2313411r325512',
        name='Module Test',
    )
    assert cl_map.insert(existing_test_cl)
    test_file = data_provider.get_module_test_change_data()
    assert sort_by_source_set(cl_map, test_file)
    # Check CL Map for File in Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    assert existing_test_cl == result[0]
    assert len(existing_test_cl.changes) == 1


def test_is_sorted_by_source_set_modulemain_cl_modulemain_file_returns_true():
    modulemain_key = list_key.compute_key('Module Main')
    test_file = data_provider.get_module_src_change_data()
    assert is_sorted_by_source_set(modulemain_key, test_file)
    

def test_is_sorted_by_source_set_module_cl_module_file_returns_false():
    module_key = list_key.compute_key('Module')
    test_file = data_provider.get_module_src_change_data()
    assert not is_sorted_by_source_set(module_key, test_file)
    

def test_is_sorted_by_source_set_moduletest_cl_moduletest_file_returns_true():
    moduletest_key = list_key.compute_key('Module Test')
    test_file = data_provider.get_module_test_change_data()
    assert is_sorted_by_source_set(moduletest_key, test_file)
    

def test_is_sorted_by_source_set_module_cl_modulemain_file_returns_false():
    module_key = list_key.compute_key('Module')
    test_file = data_provider.get_module_test_change_data()
    assert not is_sorted_by_source_set(module_key, test_file)


def test_is_sorted_by_source_set_appmain_cl_gradle_build_file_returns_false():
    app_key = list_key.compute_key('App Main')
    test_file = data_provider.get_app_gradle_build_change_data()
    assert not is_sorted_by_source_set(app_key, test_file)


def test_get_source_set_name_module_src_file_returns_src():
    test_file = data_provider.get_module_src_change_data()
    assert _get_source_set_name(test_file) == 'main'


def test_get_source_set_name_module_test_file_returns_test():
    test_file = data_provider.get_module_test_change_data()
    assert _get_source_set_name(test_file) == 'test'


def test_get_source_set_name_module_debug_file_returns_debug():
    test_file = data_provider.get_module_debug_change_data()
    assert _get_source_set_name(test_file) == 'debug'


def test_get_source_set_name_module_androidtest_file_returns_androidtest():
    test_file = data_provider.get_change_data(_ANDROID_TEST_CHANGE_PATH)
    assert _get_source_set_name(test_file) == 'androidTest'


def test_get_source_set_name_module_testfixtures_file_returns_testfixtures():
    test_file = data_provider.get_change_data(_TEST_FIXTURES_CHANGE_PATH)
    assert _get_source_set_name(test_file) == 'testFixtures'
