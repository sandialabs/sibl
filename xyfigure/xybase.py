import os
import sys
from abc import ABC

# Helper functions
def absolute_path(folder):
    """
    Makes certain the path to the folder for pending serialization exists.
    If it doesn't exist, ask the user if the folder should be created or not.
    Print the full path to the command line.
    Returns the absolute path for pending serialization.
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
    print(f'  serialized path = {abs_path}')
    return abs_path

## Abstract Base Class
class XYBase(ABC):
    """
    Base class to collect all data and methods common to XYBase descendants.
    """
    def __init__(self, **kwargs):
        self._folder = kwargs['folder']
        self._file = kwargs['file']
        self._abs_path_and_file = os.path.join('.', 'serialize_placeholder.txt')

    def serialize(self, folder, filename):
        """Contains precursors to serialized, used by all descendants."""
        abs_path = absolute_path(folder)
        # defaults to the process id
        self._abs_path_and_file = os.path.join(abs_path, filename)
