import os
import sys
from abc import ABC
# from datetime import datetime

# Helper functions
def absolute_path(folder):
    """
    Makes certain the path to the folder for pending serialization exists.
    If it doesn't exist, ask the user if the folder should be created or not.
    Print the full path to the command line.
    Returns the absolute path, possibly for pending serialization.
    """
    abs_path = os.path.join(os.getcwd(), folder)
    if not os.path.isdir(abs_path):
        print(f'Folder needed but not found: "{abs_path}"')
        val = input('Create folder? [y]es or [n]o : ')
        if val == 'y':
            os.mkdir(folder)
            print(f'Created folder: "{folder}"')
        else:
            print('Check accuracy of folders in database.')
            print('Abnormal script termination.')
            sys.exit('Folder misspecified.')
    return abs_path

## Abstract Base Class
class XYBase(ABC):
    """
    Base class to collect all data and methods common to XYBase descendants.
    """
    def __init__(self, guid, **kwargs):

        self._guid = guid

        self._serialize = kwargs.get('serialize', False) # moved up from XYView

        default_folder = "."
        self._folder = kwargs.get('folder', default_folder)

        # self._file = kwargs['file']
        # now = datetime.now()
        # now_str = now.strftime("%Y-%m-%d+%H:%M:%S")
        # default_file = now_str + '.csv'
        # self._file = kwargs.get('file', default_file)

        self._file = kwargs.get('file', None)

        if self._file is None:
            print('Error: keyword "file" not found.')
            sys.exit('Abnormal termination.')

        abs_path = absolute_path(self._folder)

        self._path_file_input = os.path.join(abs_path, self._file)
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
