"""Testing Change Data Methods.
"""
from changelist_sort.change_data import ChangeData
from test import data_provider


def test_get_sort_path_after_src_file_returns_after():
    expected = '/app/src/main/java/app/Main.java'
    test_data = ChangeData(
        after_dir=False,
        after_path=expected
    )
    result = test_data._get_sort_path()
    assert expected == result


def test_get_sort_path_before_and_after_src_files_returns_after():
    expected = '/app/src/main/java/app/Main.java'
    test_data = ChangeData(
        before_dir=False,
        before_path='/app/src/main/java/app/File.java',
        after_dir=False,
        after_path=expected
    )
    result = test_data._get_sort_path()
    assert expected == result


def test_get_sort_path_before_src_file_returns_before():
    expected = '/app/src/main/java/app/Main.java'
    test_data = ChangeData(
        before_dir=False,
        before_path=expected,
    )
    result = test_data._get_sort_path()
    assert expected == result


def test_first_dir_root_gradle_returns_none():
    cd = data_provider.get_root_gradle_build_change_data()
    assert cd.first_dir is None


def test_first_dir_app_gradle_returns_app():
    cd = data_provider.get_app_gradle_build_change_data()
    assert 'app' == cd.first_dir


def test_first_dir_module_src_returns_module():
    cd = data_provider.get_module_src_change_data()
    assert 'module' == cd.first_dir


def test_first_dir_module_test_returns_module():
    cd = data_provider.get_module_test_change_data()
    assert 'module' == cd.first_dir


def test_first_dir_gradle_properties_returns_gradle():
    cd = data_provider.get_gradle_properties_change_data()
    assert 'gradle' == cd.first_dir


def test_first_dir_github_workflows_returns_github():
    cd = data_provider.get_github_workflows_change_data()
    assert '.github' == cd.first_dir


def test_file_basename_module_src_file_returns_file():
    cd = data_provider.get_module_src_change_data()
    assert 'Main.java' == cd.file_basename


def test_file_basename_gradle_properties_returns_file():
    cd = data_provider.get_gradle_properties_change_data()
    assert 'gradle-wrapper.properties' == cd.file_basename


def test_file_basename_root_gradle_build_returns_file():
    cd = data_provider.get_root_gradle_build_change_data()
    assert 'build.gradle' == cd.file_basename


def test_file_ext_module_src_file_returns_ext():
    cd = data_provider.get_module_src_change_data()
    assert 'java' == cd.file_ext


def test_file_ext_root_gradle_build_returns_ext():
    cd = data_provider.get_root_gradle_build_change_data()
    assert 'gradle' == cd.file_ext


def test_file_ext_github_src_file_returns_ext():
    cd = data_provider.get_github_workflows_change_data()
    assert 'yml' == cd.file_ext


def test_file_ext_hidden_file_with_ext_returns_ext():
    cd = data_provider.get_change_data('/module/.hidden_file.c')
    assert 'c' == cd.file_ext


def test_file_ext_hidden_file_no_ext_returns_none():
    cd = data_provider.get_change_data('/module/.hidden_file')
    assert cd.file_ext is None


def test_file_ext_gradle_kts_returns_ext():
    cd = data_provider.get_change_data('/module/build.gradle.kts')
    assert 'gradle.kts' == cd.file_ext
