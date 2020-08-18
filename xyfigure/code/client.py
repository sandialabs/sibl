#!/usr/bin/env python
# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import sys
import json

# related third-party imports

# local application/library specific imports
# from xyfigure.factory import XYFactory
from xyfigure.code.factory import XYFactory

# from xyfigure.xymodel import XYModel
from xyfigure.code.xymodel import XYModel

# from xyfigure.xyview import XYView
from xyfigure.code.xyview import XYView


def main(argv):
    """Client to generate a XYFigure from an 'input_file.json' file.

    Preconditions:
    $ module load anaconda3
    ~/sibl/io/input_file.json  # database of XYFigure objects to create

    Use:
    $ cd ~/sibl/io/<path_containing_input_file.json>/
    $ python ~/sibl/xyfigure/client.py input_file.json

    Example Input:
    $ cd ~/sibl/io/mil_spec_paper/
    $ python ~/sibl/xyfigure/client.py MHSRS_exp_only.json

    Example Output:
    ~/sibl/io/mil_spec_paper/fig/MHSRS_exp_only.pdf  # output figure

    """

    # to do, add argparse with verbose flag, for now, hard code
    verbose = False

    help_string = "$ python ~/sibl/xyfigure/code/client.py input_file.json"
    try:
        input_file = argv[0]
    except IndexError as error:
        print(f"Error: {error}.")
        print("check script pattern: " + help_string)
        print("Abnormal script termination.")
        sys.exit("No input file specified.")

    with open(input_file) as f:
        database = json.load(f)

    items = []  # cart of items is empty, fill from factory
    # factory = XYFactory()  # it's static!

    for item in database:
        kwargs = database[item]
        i = XYFactory.create(item, **kwargs)
        if i:
            items.append(i)
        else:
            print("Item is None from factory, nothing added to Client items.")

    models = [i for i in items if isinstance(i, XYModel)]
    views = [i for i in items if isinstance(i, XYView)]

    for view in views:
        if verbose:
            print(f'Creating view with guid = "{view.guid}"')

        if view.model_keys:  # register only selected models with current view
            if verbose:
                print(f"  Adding {view.model_keys} model(s) to current view.")
            view.models = [m for m in models if m.guid in view.model_keys]
            view.figure()  # must be within this subset scope
        else:
            if verbose:
                print("  Adding all models to current view.")
            view.models = models  # register all models with current view
            view.figure()  # must be within this subset scope

    if verbose:
        print("====================================")
        print("End of xyfigure/client.py execution.")


if __name__ == "__main__":
    main(sys.argv[1:])
