# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import os
from pathlib import Path
import sys
from abc import ABC

# related third-party imports

# local application/library specific imports


# Helper functions
def absolute_path(folder):
    """
    Makes certain the path to the folder for pending serialization exists.
    If it doesn't exist, ask the user if the folder should be created or not.
    Print the full path to the command line.
    Returns the absolute path, possibly for pending serialization.
    """
    run_path = Path.cwd()
    abs_path = run_path.joinpath(folder)
    # abs_path = os.path.join(os.getcwd(), folder)
    if not os.path.isdir(abs_path):
        print(f'Folder needed but not found: "{abs_path}"')
        val = input("Create folder? [y]es or [n]o : ")
        if val == "y":
            os.mkdir(folder)
            print(f'Created folder: "{folder}"')
        else:
            print("Check accuracy of folders in database.")
            print("Abnormal script termination.")
            sys.exit("Folder misspecified.")
    return abs_path


# Abstract Base Class
class XYBase(ABC):
    """
    Base class to collect all data and methods common to XYBase descendants.
    """

    def __init__(self, guid, **kwargs):

        self._guid = guid

        self._verbose = kwargs.get("verbose", True)

        # moved up from XYView
        self._serialize = kwargs.get("serialize", False)

        default_folder = "."
        self._folder = kwargs.get("folder", default_folder)
        self._folder_pathlib = Path(self._folder).expanduser()
        if not self._folder_pathlib.is_dir():
            print('Error: keyword "folder" has a value (e.g., a folder path)')
            print("that cannot be found as specified:")
            print(self._folder_pathlib)
            raise KeyError("folder not found")

        self._file = kwargs.get("file", None)

        if self._file is None:
            print('Error: keyword "file" not found.')
            sys.exit("Abnormal termination.")

        # abs_path = absolute_path(self._folder)

        # self._path_file_input = os.path.join(abs_path, self._file)
        self._file_pathlib = self._folder_pathlib.joinpath(self._file)
        self._path_file_input = str(self._file_pathlib)
        self._path_file_output = None

    @property
    def guid(self):
        return self._guid

    def serialize(self, folder, filename):
        """
        Writes our data, to be extended by descendants.
        """
        abs_path = absolute_path(folder)
        self._path_file_output = os.path.join(abs_path, filename)
