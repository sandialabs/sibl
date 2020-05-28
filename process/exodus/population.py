#!/usr/bin/env python
import os
import sys
import json
import numpy as np
# import getpass
# import ctypes
# import exodus
# import matplotlib.pyplot as plt
# import numpy as np

def main(argv):
    """ Extracts the population of values of a variable from an Exodus
    output file.

    Client use:
    [bob-063c] $ python ../exodus_population.py gray_white_strain.json

    with prerequisties:
    $ module purge
    $ module load anaconda3
    $ module load seacas  # to make import exodus available
    $ cd /casco_sim/bob-1mm-5kg-helmet2-0305-hemi-063c
    $ epu -auto output_field.e.16.00  # e.g., merge multi-proc to one file
    """

    home = os.getcwd()
    script_name = os.path.basename(__file__)

    try:

        print('This is Python script: ' + script_name)
        print('with argument: ' + argv)

        # Look for the .json input file
        with open(argv) as jfile:
            json_file = json.load(jfile)

            # Process .json input file
            input_folder = json_file['folder']
            print(f'From folder: {input_folder}')

            input_file = json_file['file_exodus']
            print(f'  with Exodus file: {input_file}')

            tsteps = json_file['time_steps']
            print(f'  at time step(s): {tsteps}')

            blocks = json_file['blocks']
            print(f'  from block(s): {blocks}')

            variables = json_file['variables']
            print(f'  extracting variable(s) {variables}')

            output_files = []
            print(f'To the folder: {input_folder}')
            print('  extracted variable(s) to be written to file(s): ')
            for ts in tsteps:
                ofile = argv.split('.')[0] + '_ts_' + str(ts) + '.csv'
                print('    ' + ofile)
                output_files.append(ofile)

        # Execute steps extracted from exodus_extract.py
        os.chdir(input_folder)
#        database = exodus.exodus(input_file, mode='r')

        # number_of_blocks = database.num_blks()
#        number_of_ts = database.num_times()
#        nts_str = str(number_of_ts)
#        print(f'Number of time steps available from Exodus file: {nts_str}')
#
#        assert(tstep_start < number_of_ts), 'number_of_ts = ' + nts_str
#        assert(tstep_stop <= number_of_ts), 'number_of_ts = ' + nts_str
#
#        print('Variables available from Exodus file:')
#        print(database.get_element_variable_names())
#        print('Blocks available from Exodus file:')
#        print(database.get_elem_blk_names())

        for i, ts in enumerate(tsteps):
            print(f'Processing population for time step {ts}')

            data_at_time_step = []

            # accumulate variable data across all blocks
            for block in blocks:
                print(f'  processing block: {block}')

                for variable in variables:
                    print(f'    processing variable={variable}')
#                    values = database.get_element_variable_values(block, variable, ts)
                    # print('  appending ' + str(len(values)) + ' values.')
#                    for value in values:
#                        # print('value is ' + str(value))
#                        data_at_time_step.append(value)

            header_str = '# population ' + str(variables) + ' blocks '
            header_str += str(blocks) + ' at time step ' + str(ts)
            print(f'header string is {header_str}')
            np.savetxt(output_files[i], data_at_time_step, delimiter=',', header=header_str)
            print('Extracted variable(s) written to file: ' + output_files[i])

    except IndexError as error:
        print('Error: ' + str(error))
        print('Error: no input folder target specified.')

    except FileNotFoundError:
        print('Error: FileNotFound.')
        print('Could not find json file for processing: ' + argv)

    except IOError as error:
        print('Error:' + str(error))

    finally:
        os.chdir(home)
        print('\nCurrent directory: ' + home)
        print('Python script finished.')



if __name__ == "__main__":
    main(sys.argv[1])
