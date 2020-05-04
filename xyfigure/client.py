#!/usr/bin/env python
# import os
import sys
import json
# from factory import XYFactory
from xyfigure.factory import XYFactory
# from xymodel import XYModel
from xyfigure.xymodel import XYModel
# from xyview import XYView
from xyfigure.xyview import XYView


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

    help_string = '$ python ~/sibl/xyfigure/client.py input_file.json'
    try:
        input_file = argv[0]
    except IndexError as error:
        print(f'Error: {error}.')
        print('check script pattern: ' + help_string)
        print('Abnormal script termination.')
        sys.exit('No input file specified.')

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
            print('Item is None from factory, nothing added to Client items.')

    models = [i for i in items if isinstance(i, XYModel)]
    views = [i for i in items if isinstance(i, XYView)]

    for view in views:
        print(f'Creating view with guid = "{view.guid}"')
        if view.model_keys: # register only selected models with current view
            print(f'  Adding {view.model_keys} model(s) to current view.')
            view.models = [m for m in models if m.guid in view.model_keys]
            view.figure()  # must be within this subset scope
        else: 
            print('  Adding all models to current view.')
            view.models = models  # register all models with current view
            view.figure()  # must be within this subset scope

    print('=======================')
    print('End of client execution.')

if __name__ == '__main__':
    main(sys.argv[1:])
