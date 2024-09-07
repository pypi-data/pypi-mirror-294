"""Defines and Validates Argument Syntax.

Encapsulates Argument Parser.

Returns Argument Data, the args provided by the User.
"""
from argparse import ArgumentParser
from sys import exit
from typing import Optional

from .argument_data import ArgumentData
from .string_validation import validate_name


def parse_arguments(args: Optional[list[str]] = None) -> ArgumentData:
    """
    Parse command line arguments.

    Parameters:
    - args: A list of argument strings.

    Returns:
    ArgumentData : Container for Valid Argument Data.
    """
    if args is None or len(args) == 0:
        return ArgumentData(None)
    # Initialize the Parser and Parse Immediately
    try:
        parsed_args = _define_arguments().parse_args(args)
    except SystemExit:
        exit("Unable to Parse Arguments.")
    return _validate_arguments(parsed_args)


def _validate_arguments(
    parsed_args,
) -> ArgumentData:
    """
    Checks the values received from the ArgParser.
        Uses Validate Name method from StringValidation.

    Parameters:
    - parsed_args : The object returned by ArgumentParser.

    Returns:
    ArgumentData - A DataClass of syntactically correct arguments.
    """
    workspace_path = parsed_args.workspace
    if workspace_path is not None:
        if not validate_name(workspace_path):
            exit("The Workspace Path argument was invalid.")
    return ArgumentData(
        workspace_path=workspace_path,
        developer_sort=parsed_args.developer_sort,
        sourceset_sort=parsed_args.sourceset_sort,
    )


def _define_arguments() -> ArgumentParser:
    """
    Initializes and Defines Argument Parser.
       - Sets Required/Optional Arguments and Flags.

    Returns:
    argparse.ArgumentParser - An instance with all supported Arguments.
    """
    parser = ArgumentParser(
        description="Changelist Sort",
    )
    # Optional Arguments
    parser.add_argument(
        '--workspace',
        type=str,
        default=None,
        help='The Workspace File containing the ChangeList data. Searches current directory by default.'
    )
    parser.add_argument(
        '-d', '--developer_sort', '--developer-sort',
        action='store_true',
        default=False,
        help='A Flag indicating that Developer Sort is to be used primarily. Fallback to Module Sort.',
    )
    parser.add_argument(
        '-s', '--sourceset_sort', '--sourceset-sort',
        action='store_true',
        default=False,
        help='A Flag indicating that SourceSet Sort is to be used primarily. Fallback to Module Sort.',
    )
    return parser
