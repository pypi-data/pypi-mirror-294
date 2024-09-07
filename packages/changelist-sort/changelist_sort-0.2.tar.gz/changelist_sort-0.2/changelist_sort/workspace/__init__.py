""" Workspace Package.
"""
from pathlib import Path
from xml.etree.ElementTree import ParseError, fromstring

from changelist_sort.input.input_data import InputData
from changelist_sort.workspace.workspace_tree import WorkspaceTree


def get_workspace_tree(
    input_data: InputData
) -> WorkspaceTree:
    """
    Parse the Workspace XML into a Workspace Tree.

    Parameters:
    - input_data (InputData)
    """
    try:
        xml_root = fromstring(input_data.workspace_xml)  
    except ParseError:
        exit(f'Failed to Parse Workspace XML at {input_data.workspace_path}')
    return WorkspaceTree(xml_root)


def write_workspace_tree(
    ws_tree: WorkspaceTree,
    path: Path,
) -> bool:
    """
    Write the Workspace Tree as XML to the given Path.
    """
    ws_tree.get_root().write(
        file_or_filename=path,
        encoding='utf-8',
        xml_declaration=True,
        method='xml',
    )
