""" Testing Main Package Init Module Methods.
"""
from pathlib import Path
from xml.etree.ElementTree import ElementTree

import pytest

from changelist_sort.workspace.workspace_tree import WorkspaceTree
from test import data_provider
from changelist_sort import sort_changelists
from changelist_sort.input.input_data import InputData
from changelist_sort.sorting.sort_mode import SortMode


def save_write(
    self: ElementTree, file_or_filename, encoding='utf-8', xml_declaration=True,
    method='xml'
):
    global TAG
    global VERSION
    global WS_TREE
    elem = self.getroot()
    TAG = elem.tag
    VERSION = elem.attrib['version']
    WS_TREE = WorkspaceTree(elem)


def test_sort_changelists_simple_module_sort_returns_xml():
    test_input = InputData(
        workspace_path=Path('file'),
        workspace_xml=data_provider.get_simple_changelist_xml(),
        sort_mode=SortMode.MODULE,
    )
    with (pytest.MonkeyPatch().context() as c):
        c.setattr(ElementTree, 'write', save_write)
        sort_changelists(test_input)
    assert TAG == 'project'
    assert VERSION == '4'
    result = WS_TREE.extract_list_elements()
    assert len(result) == 2


def test_sort_changelists_simple_module_sort_remove_empty_returns_xml():
    test_input = InputData(
        workspace_path=Path('file'),
        workspace_xml=data_provider.get_simple_changelist_xml(),
        sort_mode=SortMode.MODULE,
        remove_empty=True,
    )
    with (pytest.MonkeyPatch().context() as c):
        c.setattr(ElementTree, 'write', save_write)
        sort_changelists(test_input)
    assert TAG == 'project'
    assert VERSION == '4'
    result = WS_TREE.extract_list_elements()
    assert len(result) == 1


def test_sort_changelists_multi_cl_returns_xml():
    test_input = InputData(
        workspace_path=Path('file'),
        workspace_xml=data_provider.get_multi_changelist_xml(),
        sort_mode=SortMode.MODULE,
    )
    with (pytest.MonkeyPatch().context() as c):
        c.setattr(ElementTree, 'write', save_write)
        sort_changelists(test_input)
    assert TAG == 'project'
    assert VERSION == '4'
    result = WS_TREE.extract_list_elements()
    assert len(result) == 3


def test_sort_changelists_multi_cl_remove_empty_returns_xml():
    test_input = InputData(
        workspace_path=Path('file'),
        workspace_xml=data_provider.get_multi_changelist_xml(),
        sort_mode=SortMode.MODULE,
        remove_empty=True,
    )
    with (pytest.MonkeyPatch().context() as c):
        c.setattr(ElementTree, 'write', save_write)
        sort_changelists(test_input)
    assert TAG == 'project'
    assert VERSION == '4'
    result = WS_TREE.extract_list_elements()
    assert len(result) == 2


def test_sort_changelists_multi_cl_sourceset_sort_returns_xml():
    test_input = InputData(
        workspace_path=Path('file'),
        workspace_xml=data_provider.get_multi_changelist_xml(),
        sort_mode=SortMode.SOURCESET,
    )
    with (pytest.MonkeyPatch().context() as c):
        c.setattr(ElementTree, 'write', save_write)
        sort_changelists(test_input)
    assert TAG == 'project'
    assert VERSION == '4'
    result = WS_TREE.extract_list_elements()
    assert len(result) == 3


def test_sort_changelists_multi_cl_sourceset_sort_remove_empty_returns_xml():
    test_input = InputData(
        workspace_path=Path('file'),
        workspace_xml=data_provider.get_multi_changelist_xml(),
        sort_mode=SortMode.SOURCESET,
        remove_empty=True,
    )
    with (pytest.MonkeyPatch().context() as c):
        c.setattr(ElementTree, 'write', save_write)
        sort_changelists(test_input)
    assert TAG == 'project'
    assert VERSION == '4'
    result = WS_TREE.extract_list_elements()
    assert len(result) == 2

