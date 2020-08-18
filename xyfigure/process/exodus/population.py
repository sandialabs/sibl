#!/usr/bin/env python
import os
import sys
import json
import numpy as np
import exodus


def main(argv):
    """ Extracts the population of values of a variable from an Exodus
    output file.

    Client use:
    [~/sibl/process/exodus] $ python population.py hx-master-ssr-population.json

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

        print("This is Python script: " + script_name)
        print("with argument: " + argv)

        # Look for the .json input file
        with open(argv) as jfile:
            json_file = json.load(jfile)

            # Process .json input file
            input_folder = json_file["folder"]
            print(f"From folder: {input_folder}")

            input_file = json_file["file_exodus"]
            print(f"  with Exodus file: {input_file}")

            tsteps = json_file["time_steps"]
            print(f"  at time step(s): {tsteps}")

            blocks = json_file["blocks"]
            print(f"  from block(s): {blocks}")

            variables = json_file["variables"]
            print(f"  extracting variable(s) {variables}")

        # Execute steps extracted from exodus_extract.py
        os.chdir(input_folder)
        database = exodus.exodus(input_file, mode="r")

        number_of_ts = database.num_times()
        print(f"Number of time steps available from Exodus file: {number_of_ts}")

        print("Variables available from Exodus file:")
        print(database.get_element_variable_names())
        print("Blocks available from Exodus file:")
        print(database.get_elem_blk_names())

        for ts in tsteps:
            print(f"Processing population for time step {ts}")

            for block in blocks:
                print(f"  processing block: {block}")

                for variable in variables:
                    print(f"    processing variable={variable}")
                    values = database.get_element_variable_values(block, variable, ts)

                    header_str = (
                        "ts_" + str(ts) + "_block_" + str(block) + "_" + str(variable)
                    )
                    output_file = header_str + ".txt"
                    np.savetxt(output_file, values, delimiter=",", header=header_str)
                    print(f"      extracted variable to file: {output_file}")

    except IndexError as error:
        print("Error: " + str(error))
        print("Error: no input folder target specified.")

    except FileNotFoundError:
        print("Error: FileNotFound.")
        print("Could not find json file for processing: " + argv)

    except IOError as error:
        print("Error:" + str(error))

    finally:
        os.chdir(home)
        print("\nCurrent directory: " + home)
        print("Python script finished.")


if __name__ == "__main__":
    main(sys.argv[1])
