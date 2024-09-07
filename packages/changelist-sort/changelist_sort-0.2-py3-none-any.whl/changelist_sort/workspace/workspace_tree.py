""" The Workspace Element Tree Methods.
"""
from xml.etree.ElementTree import Element, ElementTree, indent

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.workspace.xml_reader import _read_bool_from, filter_by_tag, get_attr, get_attr_or


class WorkspaceTree:
    """
    Manages the Workspace XML Element Trees.

    Properties:
    - xml_root (Element): The XML root element.
    - changelist_manager (Element): The Changelist Manager Component Element.
    """

    def __init__(
        self,
        xml_root: Element,
    ):
        self._xml_root = xml_root
        self.changelist_manager = _find_changelist_manager(xml_root)

    def extract_list_elements(self) -> list[ChangelistData]:
        """
        Given the Changelist Manager Element, obtain the list of List Elements.

        Parameters:
        - changelist_manager (ElementTree): The ChangeList Manager XML Element.

        Returns:
        list[Element] - A List containing the Lists.
        """
        if self.changelist_manager is None:
            exit('XML File does not have a Changelist Manager.')
        return [
            ChangelistData(
                id=get_attr(cl_element, 'id'),
                name=get_attr(cl_element, 'name'),
                changes=_extract_change_data(cl_element),
                comment=get_attr_or(cl_element, 'comment', ''),
                is_default=_read_bool_from(cl_element, 'default'),
            ) for cl_element in filter_by_tag(self.changelist_manager, 'list')
        ]

    def replace_changelists(
        self,
        changelists: list[ChangelistData]
    ):
        """
        Replace the XML Tree's Changelist Manager Lists.
        """
        clm = self.changelist_manager
        if clm is None:
            exit('XML File does not have a Changelist Manager.')
        # First obtain all Option Elements
        options = list(clm.findall('option'))
        # Clear the Changelist Manager Tag
        clm.clear()
        # Need to Add Name Attribute after Clear
        clm.attrib['name'] = "ChangeListManager"
        clm.extend(_write_list_element(x) for x in changelists)
        clm.extend(options)
        indent(clm, level=1)

    def get_root(self) -> ElementTree:
        """
        Obtain the XML ElementTree Root.
        """
        return ElementTree(self._xml_root)


def _find_changelist_manager(xml_root: Element) -> Element | None:
    """
    Try to find the Changelist Manager in the XML ElementTree.
    """
    cl_manager = None
    for elem in filter_by_tag(xml_root, 'component'):
        try:
            if elem.attrib["name"] == 'ChangeListManager':
                cl_manager = elem
                break
        except KeyError:
            pass
    return cl_manager


def _extract_change_data(
    list_element: Element,
) -> list[ChangeData]:
    """
    Given a ChangeList XML Element, obtain the List of Changes.

    Parameters:
    - list_element (Element): The Element representing a Changelist.

    Returns:
    list[ChangeData] - The list of structured ChangeData.
    """
    return [
        ChangeData(
            before_path=_filter_project_dir(get_attr(change, 'beforePath')),
            before_dir=_convert_bool(get_attr(change, 'beforeDir')),
            after_path=_filter_project_dir(get_attr(change, 'afterPath')),
            after_dir=_convert_bool(get_attr(change, 'afterDir')),
        ) for change in filter(lambda x: x.tag == 'change', list_element)
    ]


def _write_list_element(
    changelist: ChangelistData,
) -> Element:
    """
    Convert a Changelist to XML Element format.

    Parameters:
    - changelist (ChangelistData): The Changelist data to format.

    Returns:
    str - A String containing the xml formatted contents of the Changelist. 
    """
    clist = Element('list')
    if changelist.is_default:
        clist.set('default', 'true')
    clist.set('id', changelist.id)
    clist.set('name', changelist.name)
    clist.set('comment', changelist.comment)
    for change in changelist.changes:
        clist.append(_write_change_data(change))
    indent(clist, level=2)
    return clist


def _write_change_data(
    data: ChangeData
) -> Element:
    """
    Write the Change Data to XML format.

    Parameters:
    - data (ChangeData): The Change Data for a specific File.

    Returns:
    str - A String containing the XML tag for this Change Data.
    """
    change = Element('change')
    if data.before_path is not None:
        change.set('beforePath', _PROJECT_DIR_VAR + data.before_path)
    if data.before_dir is not None:
        change.set('beforeDir', str(data.before_dir).lower())
    if data.after_path is not None:
        change.set('afterPath', _PROJECT_DIR_VAR + data.after_path)
    if data.after_dir is not None:
        change.set('afterDir', str(data.after_dir).lower())
    #
    indent(change, level=3)
    return change


_PROJECT_DIR_VAR = '$PROJECT_DIR$'
_PROJECT_DIR_LEN = len(_PROJECT_DIR_VAR)


def _filter_project_dir(path_str: str | None) -> str | None:
    """
    Filter the ProjectDir string at the beginning of the path.
    """
    if path_str is None:
        return None
    if path_str.startswith(_PROJECT_DIR_VAR):
        return path_str[_PROJECT_DIR_LEN:]
    return path_str


def _convert_bool(attr: str | None) -> bool | None:
    """
    Convert a String attribute to boolean.
    """
    if attr is None:
        return None
    return attr == 'true'
