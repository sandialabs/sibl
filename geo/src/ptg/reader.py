"""This module provide command line reading of .yml file types.
"""

from pathlib import Path

# import sys
# import json
import yaml
from typing import Tuple, Union, List, Any
from functools import reduce


class Reader:
    def __init__(self, *, input_file: str):
        """The reader performs input of client input files in YAML format.

        Arguments:
            input_file (string): The fully pathed input file, as a string.
                Example:  "C:/Users/client/projecxt/my_input.yml"

        Attributes:
            database (dict): The contents of the input_file read in as a dictionary.
                Defaults to an empty dictionary.
            initialized (bool): Convenience attribute for clients to know if the
                input_file has been successfully read into the Reader's database.

        Raises:
            OSError: If the input_file is not found.
            TypeError: If the input_file is not of type `.yml` or `.yaml`.
        """
        self.initialized = False  # default, the database has not yet been populated

        # path_file_in = Path(argv[0]).resolve()
        # self.path_file_in = Path(input_file).resolve()
        path_file_in = Path(input_file).resolve()

        # self.file_type = (
        #     self.path_file_in.suffix
        # )  # returns "json" from "input_example.json"
        # file_type = path_file_in.suffix  # returns "json" from "input_example.json"

        # if not self.path_file_in.is_file():
        #     raise OSError(f"File not found: {self.path_file_in}")
        if not path_file_in.is_file():
            raise OSError(f"File not found: {path_file_in}")

        # Compared to the lower() method, the casefold() method is stronger.
        # It will convert more characters into lower case, and will find more matches
        # on comparison of two strings that are both are converted
        # using the casefold() method.
        file_type = path_file_in.suffix.casefold()

        supported_types = (".yaml", ".yml")

        if file_type not in supported_types:
            raise TypeError("Only file types .yaml, and .yml are supported.")

        try:
            # with open(self.path_file_in, "r") as stream:
            with open(path_file_in, "r") as stream:
                # self.database = yaml.safe_load(stream)
                # self.database = yaml.load(stream)
                # See deprecation warning for plain yaml.load(input) at
                # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
                self.database = yaml.load(stream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as error:
            print(f"Error with YAML file: {error}")
            # print(f"Could not open: {self.path_file_in}")
            int(f"Could not open or decode: {path_file_in}")
            # raise yaml.YAMLError
            raise OSError

        # manadating that files read in have at least these five keys
        required_keys = ("version", "boundary")
        has_required_keys = all(
            tuple(map(lambda x: self.database.get(x), required_keys))
        )
        if not has_required_keys:
            raise KeyError(f"Input files must have these keys defined: {required_keys}")

        # determine if self.database is monolithic dict or contains pointers to subfiles
        # self.database = aggregate(database=self.database)

        print(f"input: {path_file_in}")
        self.initialized = True

    def extract(self, *, key: str) -> dict:
        """
        Extracts a specific part of the .yml input file,
        raises KeyError if bad key is attempted.
        """

        try:
            return self.database[key]

        except KeyError:
            print(f"Key: {key}, does not exist")
            return {}

    def extract_deep(self, *, keys: Tuple[str, ...]) -> Union[Any, List[Any]]:
        """
        Extracts a specific part of the .yml input file,
        raises KeyError if bad key sequence is attempted.
        """

        # zz = reduce(lambda d, key: d.get(key) if d else None, keys, self.database)

        try:
            item = reduce(lambda x, y: x.get(y) if x else None, keys, self.database)
            if item is not None:
                return item
            else:
                raise KeyError

        except KeyError:
            print("Key(s): does(do) not exist:")
            for key in keys:
                print(f"{key}")
            return {}
