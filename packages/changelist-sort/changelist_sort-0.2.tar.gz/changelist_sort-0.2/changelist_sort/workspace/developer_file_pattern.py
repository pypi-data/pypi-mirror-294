""" Developer Files Definitions.
    Add New Types of Pattern Implementations Here.
"""
from typing import Callable

from changelist_sort.change_data import ChangeData


class DeveloperFilePattern:
    """
    A File Pattern to be controlled by the Developer.
    
    Properties:
    - module_type (ModuleType | None): Type of Module that this Pattern applies to.
    - _check_file (Callable[[ChangeData], bool]): Determines if the Change matches the pattern.
    """

    def __init__(self,
        inverse: bool = False,
        *args, **kwargs
    ):
        """
        Positional Arguments:
        - module_type (ModuleType | None): The Type of Module that this Pattern applies to. None applies to all.
        
        Keyword Arguments:
        - file_ext (str): The File Extension to Match.
        - first_dir (str): The First Directory in the File Path to Match.
        - filename_prefix (str): Match the Filename Prefix, ignoring first slash character.
        - filename_suffix (str): Match the Filename Suffix, ignoring file extension.
        - path_start (str): Match the start of the File Path, ignoring first slash character.
        - path_end (str): Match the end of the File Path Parent Directory, ignoring the end slash character.
        """
        self.inverse = inverse
        if 'file_ext' in kwargs:
            self._check_file = _match_file_ext(kwargs['file_ext'])
        elif 'first_dir' in kwargs:
            self._check_file = _match_first_dir(kwargs['first_dir'])
        elif 'filename_prefix' in kwargs:
            self._check_file = _match_filename_prefix(kwargs['filename_prefix'])
        elif 'filename_suffix' in kwargs:
            self._check_file = _match_filename_suffix(kwargs['filename_suffix'])
        elif 'path_start' in kwargs:
            self._check_file = _match_path_start(kwargs['path_start'])
        elif 'path_end' in kwargs:
            self._check_file = _match_path_end(kwargs['path_end'])
        # TODO: Add More Patterns To Constructor Keyword Arguments Here!
        # elif '' in kwargs:
        #   self._check_file = _match_your_new_pattern(kwargs[''])
        else:
            raise ValueError("One of the pattern matching keyword arguments must be provided.")

    def check_file(self, file: ChangeData) -> bool:
        """
        Determine if this File ChangeData matches the DeveloperFile Pattern.
        """
        return self.inverse.__xor__(self._check_file(file))


def _match_file_ext(
    file_ext: str,
) -> Callable[[ChangeData], bool]:
    """
    Match the given File Extension.
    """
    return lambda change_data: change_data.file_ext == file_ext


def _match_first_dir(
    first_dir: str | None,
) -> Callable[[ChangeData], bool]:
    """
    Match the given First Directory in the File Path.
    """
    return lambda change_data: change_data.first_dir == first_dir


def _match_filename_prefix(
    prefix: str,
) -> Callable[[ChangeData], bool]:
    """
    Match the Filename Prefix, ignoring first slash character.
    - Applies an internal function to overcome lambda limitations
    """
    return lambda change_data: change_data.file_basename.startswith(prefix)


def _match_filename_suffix(
    suffix: str,
) -> Callable[[ChangeData], bool]:
    """
    Match the Filename Suffix, ignoring file extension.
    - Applies an internal function to overcome lambda limitations
    """
    def get_filename(change_data: ChangeData) -> str:
        # Quickly return empty values
        if (filename := change_data.file_basename) == '':
            return ''
        if change_data.file_ext is not None:
            # Remove File Ext from basename
            filename = filename.removesuffix(change_data.file_ext)[:-1] # Remove file ext dot
        return filename
    # End Inner Function Definition
    return lambda change_data: get_filename(change_data).endswith(suffix)


def _match_path_start(
    path_start: str,
) -> Callable[[ChangeData], bool]:
    if not path_start.startswith('/'):
        return lambda change_data: change_data.sort_path[1:].startswith(path_start)
    else:
        return lambda change_data: change_data.sort_path.startswith(path_start)


def _match_path_end(
    path_end: str,
) -> Callable[[ChangeData], bool]:
    return lambda change_data: change_data.sort_path[:-len(change_data.file_basename)-1].endswith(path_end)


# TODO: Create Your Pattern Callables!
# Refer to ChangeData class for available pattern matching data
#
#def _match_your_new_pattern(
#    pattern_input: str,
#) -> Callable[[ChangeData], bool]:
#    return lambda change_data: False
