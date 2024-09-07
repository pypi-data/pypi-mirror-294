""" Testing Main Package Init Module Methods.
"""
from pathlib import Path
from xml.etree.ElementTree import ElementTree

import pytest

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
    elem = self.getroot()
    TAG = elem.tag
    VERSION = elem.attrib['version']


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
