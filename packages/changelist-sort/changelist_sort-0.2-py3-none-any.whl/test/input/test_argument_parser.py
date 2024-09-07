"""Testing Argument Parser Methods.
"""
from changelist_sort.input.argument_parser import parse_arguments


def test_parse_arguments_empty_list_returns_none():
    result = parse_arguments()
    assert result.workspace_path is None


def test_parse_arguments_empty_str_returns_none():
    result = parse_arguments('')
    assert result.workspace_path is None


def test_parse_arguments_change_list_main_empty_workspace_arg():
    try:
        parse_arguments(['--workspace', ''])
        assert False
    except SystemExit:
        assert True


def test_parse_arguments_change_list_main():
    result = parse_arguments(['--workspace', 'workspace.xml'])
    assert result.workspace_path == 'workspace.xml'


def test_parse_arguments_developer_sort_short_flag():
    result = parse_arguments(['-d'])
    assert result.workspace_path is None
    assert result.developer_sort
    assert not result.sourceset_sort


def test_parse_arguments_developer_sort_long():
    result = parse_arguments(['--developer-sort'])
    assert result.workspace_path is None
    assert result.developer_sort
    assert not result.sourceset_sort


def test_parse_arguments_developer_sort_long2():
    result = parse_arguments(['--developer_sort'])
    assert result.workspace_path is None
    assert result.developer_sort
    assert not result.sourceset_sort


def test_parse_arguments_sourceset_short_flag():
    result = parse_arguments(['-s'])
    assert result.workspace_path is None
    assert not result.developer_sort
    assert result.sourceset_sort


def test_parse_arguments_sourceset_long():
    result = parse_arguments(['--sourceset-sort'])
    assert result.workspace_path is None
    assert not result.developer_sort
    assert result.sourceset_sort


def test_parse_arguments_sourceset_long2():
    result = parse_arguments(['--sourceset_sort'])
    assert result.workspace_path is None
    assert not result.developer_sort
    assert result.sourceset_sort
