""" Testing Change Sort Module Methods
"""
from test import data_provider

from changelist_sort.change_data import ChangeData
from changelist_sort.sorting.file_sort import get_module_name, get_module_type
from changelist_sort.sorting.module_type import ModuleType


def test_get_module_name_empty_returns_none():
    assert get_module_name(ChangeData()) is None


def test_get_module_name_requirements_file_returns_module():
    assert 'root' == get_module_name(
        data_provider.get_change_data('requirements.txt')
    )


def test_get_module_name_setup_file_returns_module():
    assert 'root' == get_module_name(
        data_provider.get_change_data('setup.py')
    )


def test_get_module_name_src_file_returns_module():
    assert 'module' == get_module_name(
        data_provider.get_module_src_change_data()
    )
    

def test_get_module_name_test_file_returns_module():
    assert 'module' == get_module_name(
        data_provider.get_module_test_change_data()
    )


def test_get_module_name_app_build_file_returns_app():
    assert 'gradle' == get_module_name(
        data_provider.get_app_gradle_build_change_data()
    )


def test_get_module_name_root_build_file_returns_root():
    assert 'gradle' == get_module_name(
        data_provider.get_root_gradle_build_change_data()
    )


def test_get_module_name_github_workflows_returns_github():
    assert 'github' == get_module_name(
        data_provider.get_github_workflows_change_data()
    )


def test_get_module_name_github_dependabot_returns_github():
    assert 'github' == get_module_name(
        data_provider.get_github_dependabot_change_data()
    )


def test_get_module_type_root_gradle_returns_gradle():
    assert ModuleType.GRADLE == get_module_type(
        data_provider.get_root_gradle_build_change_data()
    )


def test_get_module_type_root_gradle_kts_returns_gradle():
    assert ModuleType.GRADLE == get_module_type(data_provider.get_change_data(
        '/build.gradle.kts'
    ))


def test_get_module_type_gradle_properties_returns_gradle():
    assert ModuleType.GRADLE == get_module_type(data_provider.get_change_data(
        data_provider.GRADLE_PROPERTIES_PATH
    ))


def test_get_module_type_app_build_file_returns_module():
    assert ModuleType.GRADLE == get_module_type(
        data_provider.get_app_gradle_build_change_data()
    )


def test_get_module_type_app_src_file_returns_module():
    assert ModuleType.MODULE == get_module_type(data_provider.get_change_data(
        '/app/src/main/java/com/example/app/Main.java'
    ))


def test_get_module_type_app_test_file_returns_module():
    assert ModuleType.MODULE == get_module_type(data_provider.get_change_data(
        '/app/src/test/java/com/example/app/Main.java'
    ))


def test_get_module_type_app_res_file_returns_module():
    assert ModuleType.MODULE == get_module_type(data_provider.get_change_data(
        '/app/src/main/res/values/strings.xml'
    ))


def test_get_module_type_github_workspace_returns_hidden():
    assert ModuleType.HIDDEN == get_module_type(data_provider.get_change_data(
        data_provider.GITHUB_WORKFLOW_PATH
    ))
