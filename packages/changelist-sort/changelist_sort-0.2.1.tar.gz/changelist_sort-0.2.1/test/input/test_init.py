""" Testing Input Package Init Module Methods.
"""
import pytest
from pathlib import Path

from changelist_sort.input import validate_input
from changelist_sort.sorting.sort_mode import SortMode
from test import data_provider


def test_validate_input_no_args_ws_file_does_not_exist_raises_exit():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_no_args_ws_file_is_empty_raises_exit():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: '')
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_no_args_ws_file_has_no_cl_():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert len(result.workspace_xml) > 1
        


def test_validate_input_no_args_ws_file_simple_cl_():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_simple_changelist_xml())
        result = validate_input(test_input)
        assert len(result.workspace_xml) > 1


def test_validate_input_ws_path_arg_is_empty_raises_exit():
    test_input = ['--workspace', '']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_is_missing_raises_exit():
    test_input = ['--workspace']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_does_not_exist_raises_exit():
    test_input = ['--workspace', '/file.xml']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_developer_sort():
    test_input = ['-d']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert result.workspace_path == Path('.idea/workspace.xml')
        assert result.sort_mode == SortMode.DEVELOPER


def test_validate_input_sourceset_sort():
    test_input = ['-s']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert result.workspace_path == Path('.idea/workspace.xml')
        assert result.sort_mode == SortMode.SOURCESET


def test_validate_input_remove_empty():
    test_input = ['-r']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert result.workspace_path == Path('.idea/workspace.xml')
        assert result.sort_mode == SortMode.MODULE
        assert result.remove_empty
