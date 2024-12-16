"""This module, xyfigure.py, is the new command line entry point, which
accepts input files of type .yml (instead of type .json, as done with
client.py).
"""

import argparse
from pathlib import Path

import yaml

# import xyfigure.constants as cc


def process(yml_path_file: Path) -> bool:
    """Given a .yml file, processes it to create a figure.

    Args:
        yml_path_file: The fully pathed input file.

    Returns
        True if successful, False otherwise.
    """
    processed = False

    # Compared to the lower() method, the casefold() method is stronger.
    # It will convert more characters into lower case, and will find more
    # matches on comparison of two strings that are both are converted
    # using the casefold() method.
    file_type = yml_path_file.suffix.casefold()

    supported_types = (".yaml", ".yml")

    if file_type not in supported_types:
        raise TypeError("Only file types .yaml, and .yml are supported.")

    try:
        with open(file=yml_path_file, mode="r", encoding="utf-8") as stream:
            # See deprecation warning for plain yaml.load(input) at
            # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            db = yaml.load(stream, Loader=yaml.SafeLoader)
    except yaml.YAMLError as error:
        print(f"Error with YAML file: {error}")
        # print(f"Could not open: {self.self.path_file_in}")
        print(f"Could not open or decode: {yml_path_file}")
        # raise yaml.YAMLError
        raise OSError from error

    found_keys = tuple(db.keys())
    breakpoint()

    aa = 4
    processed = True  # overwrite
    return processed  # success if we reach this line


def main():
    """Runs the module from the command line."""
    # print(cl.BANNER)
    # print(cl.CLI_DOCS)
    parser = argparse.ArgumentParser(
        prog="cthin",
        description="Generate an xyfigure.",
        epilog="xyfigure finished",
    )
    parser.add_argument(
        "input_file", help="the .yml recipe used to create the xyfigure"
    )

    args = parser.parse_args()
    if args.input_file:
        aa = Path(args.input_file).expanduser()
        if aa.is_file():
            print(f"Processing file: {aa}")
            process(yml_path_file=aa)
        else:
            print(f"Error: could not find file: {aa}")


if __name__ == "__main__":
    main()
