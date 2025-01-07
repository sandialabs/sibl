"""
This module produces the strain versus strain rate populations, with bivariate
histograms.

Example:
    > cd ~/sibl/cli/process/exodus
    > conda activate siblenv
    > python visualization.py
"""

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# import pandas as pd
import seaborn as sns


np.random.seed(0)
sns.set(style="white", color_codes=True)

EXEMPLAR = 0  # turn on or off the exemplar problem
TEST = 0  # turn on or off Bob test with small data set
TRANSLATION = (
    1  # turns on or off translational case (Bob-063f), else does rotation (Bob-066b)
)
INJURY_0 = 0  # turn on or off cellular injury curve, original
INJURY_1 = 1  # updated Summey injury curves
FIG_NAME = os.path.basename(__file__).split(".")[0]  # remove the .py extension
FIG_FORMAT = "png"  # "pdf" or "png", but "tiff" doesn't look good
DPI = 600
LATEX = 1
SERIALIZE = 1  # turn on or off write figure to disk

# sns.axes_style("darkgrid")
sns.set(style="darkgrid")
bbox_props = dict(boxstyle="square, pad=0.2", fc="white", ec="black", lw=1)

if LATEX:
    # rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
    rc("text", usetex=True)
    rc("font", family="serif")

# matplotlib.rcParams.update({'font.size': 22})
# rcParams.update({"font.size": 16})
# 2021-05-10: Increase base font size.  Process for smaller pdf files:
# 1. Generate original pdf file (about 19 MB).
# 2. Open original pdf file in Preview, save as tiff, at 600 dpi (about 56 MB)
# 3. Open tiff, export as pdf (results in 1.7 MB)
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIG_SIZE = 14

plt.rc("font", size=BIG_SIZE)  # controls default text sizes
# plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=BIG_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=BIG_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=BIG_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=BIG_SIZE)  # legend fontsize
# plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title


def cell_death_strain_rate_to_strain(x):
    # The Summey cell death curve used for production-ready figures
    y_cell_death = 0.128 * x ** (-0.156)
    return y_cell_death


# Exemplar joint distribution plot - begin
if EXEMPLAR:
    tips = sns.load_dataset("tips")

    tip_data = np.array(tips["tip"])
    bill_data = np.array(tips["total_bill"])

    # legend_txt = 'hello'
    # legend_properties = {'weight': 'bold', 'size': 12}

    g = sns.JointGrid(x=bill_data, y=tip_data)
    # g = g.plot_joint(plt.scatter, s=10, linewidths=0.05, edgecolors='blue', marker='o', alpha=0.3, label=legend_txt)
    g = g.plot_joint(
        plt.scatter,
        s=10,
        linewidths=0.05,
        edgecolors="blue",
        marker="o",
        alpha=0.3,
    )

    _ = g.ax_marg_x.hist(bill_data, color="b", bins=np.arange(0, 60, 5))
    _ = g.ax_marg_y.hist(
        tip_data, color="g", orientation="horizontal", bins=np.arange(0, 12, 1)
    )
    # _ = g.ax_joint.legend(prop=legend_properties, loc='upper left')
    _ = g.ax_joint.text(20, 10, "hello", ha="left", va="bottom", bbox=bbox_props)

    # axis_txt = f"exemplar"
    axis_txt = "exemplar"

    plt.xlabel("total bill")
    plt.ylabel("tip")

    plt.show()
    # Exemplar joint distribution plot - end

else:

    # -------------------------------- ##
    # Client application initializaton - begin
    script_pth = os.getcwd()

    # Client application initializaton - end
    # -------------------------------- ##

    if TEST:
        simulation_path = "."  # here, in same location as visualization.py
        idx = 0  # index for the probes
        probes = {
            "steps": [0],
            "time": [0.00],
            "strain_p95": [0.015],
            "strain_rate_p95": [30],
        }
        axis_txt = f'time = {probes["time"][idx] * 1000:.3f} ms (Bob-TEST-1000-pts)'
        blocks = [7]
        labels = ["white matter"]
        colors = ["C1"]  # white plotted as orange, gray -> green
        strain_files = [["test_ebe_max_principal_log_strain_51_small.txt"]]
        strain_rate_files = [
            ["test_ebe_max_principal_rate_of_deformation_51_small.txt"]
        ]
        marker_dict = {
            "linestyle": "",
            "marker": ".",
            "markersize": 10,
            "alpha": 0.2,
        }

    else:
        # not Bob TEST data subset, is the actual full data set, either translation or rotation

        # block 7 is white matter is 504,505 data points
        # block 8 is gray matter is 790,102 data points
        # combined white + gray = 1,294,607 data points

        # markers are very small and light to cope with the large data set
        marker_dict = {
            "linestyle": "",
            "marker": ",",
            "markersize": 0.7,
            "alpha": 0.2,
        }

        blocks = [7, 8]
        labels = ["white matter", "gray matter"]
        colors = ["C1", "C2"]  # white plotted as orange, gray -> green

        if TRANSLATION:

            # relative to this script, location of the particular simulation
            simulation_path = (
                "../../../../casco_sim/bob-1mm-5kg-helmet2-0305-hemi-063f/"
            )

            idx = 0  # index for the probes
            probes = {
                "steps": [30, 51, 57],
                "time": [
                    0.00580000428262166,
                    0.010000030740917116,
                    0.011200009903610695,
                ],
                "strain_p95": [
                    0.013038920686082887,
                    0.007864328738051788,
                    0.009356105757136385,
                ],
                "strain_rate_p95": [
                    26.62451150429535,
                    45.64035758617126,
                    47.167653798895905,
                ],
            }

            # axis_txt = f'time = {probes["time"][idx]*1000:.3f} ms (Bob-063f)'
            axis_txt = f'time = {probes["time"][idx] * 1000:.2f} ms'

            strain_files = [
                [
                    "ts_30_block_7_max_principal_green_lagrange_strain.txt",
                    "ts_30_block_8_max_principal_green_lagrange_strain.txt",
                ],
                [
                    "ts_51_block_7_max_principal_green_lagrange_strain.txt",
                    "ts_51_block_8_max_principal_green_lagrange_strain.txt",
                ],
                [
                    "ts_57_block_7_max_principal_green_lagrange_strain.txt",
                    "ts_57_block_8_max_principal_green_lagrange_strain.txt",
                ],
            ]

            strain_rate_files = [
                [
                    "ts_30_block_7_max_principal_green_lagrange_strain_rate.txt",
                    "ts_30_block_8_max_principal_green_lagrange_strain_rate.txt",
                ],
                [
                    "ts_51_block_7_max_principal_green_lagrange_strain_rate.txt",
                    "ts_51_block_8_max_principal_green_lagrange_strain_rate.txt",
                ],
                [
                    "ts_57_block_7_max_principal_green_lagrange_strain_rate.txt",
                    "ts_57_block_8_max_principal_green_lagrange_strain_rate.txt",
                ],
            ]

        else:  # not a TRANSLATION, then the rotation case
            simulation_path = (
                "../../../../casco_sim/bob-1mm-5kg-helmet2-0305-hemi-066b/"
            )

            idx = 1  # index for the probes
            probes = {
                "steps": [43, 69],
                "time": [0.00840000000000000, 0.013600000000000000],
                "strain_p95": [0.021800000000000000, 0.056370000000000000],
                "strain_rate_p95": [10.60000000000000, 5.190000000000000],
            }

            # axis_txt = f'time = {probes["time"][idx]*1000:.3f} ms (Bob-066b)'
            axis_txt = f'time = {probes["time"][idx] * 1000:.1f} ms'

            strain_files = [
                ["max_principal_green_lagrange_strain_ts_43.csv"],
                ["max_principal_green_lagrange_strain_ts_69.csv"],
            ]

            strain_rate_files = [
                ["max_principal_green_lagrange_strain_rate_ts_43.csv"],
                ["max_principal_green_lagrange_strain_rate_ts_69.csv"],
            ]

    # User Input Deck, simulation-specific input - end
    # -------------------------------- ##

    # fig, ax = plt.subplots(figsize=(8,8))
    # ax.set_aspect("equal")
    strain = np.array([])
    strain_rate = np.array([])

    # for i, (s, sr) in enumerate(zip(strain_files, strain_rate_files)):
    for s, sr in zip(
        strain_files[idx], strain_rate_files[idx]
    ):  # collect over all blocks

        block_strain = np.genfromtxt(os.path.join(simulation_path, s))
        block_strain_rate = np.genfromtxt(os.path.join(simulation_path, sr))
        strain = np.concatenate((strain, block_strain))
        strain_rate = np.concatenate((strain_rate, block_strain_rate))

    g = sns.JointGrid(x=strain_rate, y=strain)
    # g = g.plot_joint(plt.plot, linestyle='', marker=',', markersize=0.7, alpha=0.2)
    g = g.plot_joint(plt.plot, **marker_dict)

    exp_min = -1  # x-domain minimum 10^exp_min
    exp_max = 3  # x-domain maximum 10^exp_max
    npts = 24  # number of points

    strain_rate_095th = np.percentile(strain_rate, 95.0)  # 95th percentile strain rate
    x_bins = np.logspace(exp_min, exp_max, 2 * npts)
    _ = g.ax_marg_x.hist(strain_rate, bins=x_bins)

    strain_095th = np.percentile(strain, 95.0)  # 95th percentile strain
    strain_min = np.amin(strain)
    strain_max = np.amax(strain)
    y_bins = np.linspace(strain_min, strain_max, npts)
    _ = g.ax_marg_y.hist(strain, orientation="horizontal", bins=y_bins)

    g.ax_joint.set_xscale("log")
    g.ax_marg_x.set_xscale("log")
    g.ax_joint.set_xlim([0.01, 10000])
    # g.ax_joint.set_xlim([10**exp_min, 10**exp_max])
    g.ax_joint.set_ylim([-0.02, 0.10])

    # g.ax_joint.text(0.02, 0.09, axis_txt, ha='left', va='bottom', bbox=bbox_props)
    time_label_x = 0.02  # strain rate
    time_label_y = -0.015  # strain
    g.ax_joint.text(
        time_label_x,
        time_label_y,
        axis_txt,
        ha="left",
        va="bottom",
        bbox=bbox_props,
    )

    # draw 95th percentile boundaries
    line_prop = dict(color="orange", linewidth=1)
    # vertical line on joint plot
    g.ax_joint.plot(
        [strain_rate_095th, strain_rate_095th],
        g.ax_joint.get_ylim(),
        **line_prop,
    )

    # horizontal line on the joint plot
    g.ax_joint.plot(g.ax_joint.get_xlim(), [strain_095th, strain_095th], **line_prop)

    # vertical line across marginal strain rate plot
    y0_log_sr, y1_log_sr = g.ax_marg_x.get_ylim()
    g.ax_marg_x.plot(
        [strain_rate_095th, strain_rate_095th],
        [y0_log_sr, y1_log_sr],
        **line_prop,
    )
    # marginal strain rate text
    if TRANSLATION:
        # strain_rate_txt = r" 95\% = " + str(round(strain_rate_095th, 1))  # 26.6
        strain_rate_txt = "{:.{}f}".format(strain_rate_095th, 1)  # 26.6
    else:  # then rotation
        # strain_rate_txt = r" 95\% = " + str(round(strain_rate_095th, 2))  # 5.2, not 5.20 as desired
        strain_rate_txt = "{:.{}f}".format(strain_rate_095th, 2)  # 5.20
    # g.ax_marg_x.text(strain_rate_095th, (y0_log_sr + y1_log_sr) / 2.0, ' 95% = ' + str(round(strain_rate_095th, 1)), ha='left', va='bottom')
    g.ax_marg_x.text(
        strain_rate_095th,
        (y0_log_sr + y1_log_sr) / 2.0,
        r" 95\% = " + strain_rate_txt,
        ha="left",
        va="bottom",
    )

    # horizontal line on the marginal strain plot
    x0_strain, x1_strain = g.ax_marg_y.get_xlim()
    g.ax_marg_y.plot([x0_strain, x1_strain], [strain_095th, strain_095th], **line_prop)
    # marginal strain text
    if TRANSLATION:
        # strain_txt = r"95\% = " + str(round(strain_095th, 4))  # 0.0130
        strain_txt = "{:.{}f}".format(strain_095th, 4)  # 0.0130
    else:  # then rotation
        # strain_txt = r"95\% = " + str(round(strain_095th, 4))  # 0.0564
        strain_txt = "{:.{}f}".format(strain_095th, 4)  # 0.0564

    g.ax_marg_y.text(
        (x0_strain + x1_strain) / 2.0,
        strain_095th,
        # strain_txt,
        r" 95\% = " + strain_txt,
        ha="center",
        va="bottom",
    )

    # 2021-05-10: These seem not to work with new library, so just accept defaults.
    # g.ax_joint.grid(color="gray")
    # # g.ax_joint.grid(color="red")
    # # g.ax_joint(grid_color="red")
    # g.ax_marg_x.grid(color="green", axis="x")
    # g.ax_marg_y.grid(color="gray", axis="y")

    # plt.xlabel("max(eig(GL strain rate)) (1/s)")
    plt.xlabel("maximum principal strain rate (1/s)")
    # plt.ylabel("max(eig(GL strain)) (cm/cm)")
    plt.ylabel("maximum principal strain (cm/cm)")

    if INJURY_0 or INJURY_1:
        exp_min = -2  # x-domain minimum 10^exp_min
        exp_max = 4  # x-domain maximum 10^exp_max
        npts = 100  # number of points
        # x = np.linspace(-4, 4, npts)
        x = np.logspace(exp_min, exp_max, npts)

        # injury curves
        if INJURY_0:
            # pathway-induced injury
            # y_pathway = 0.2589 * np.arctan(-0.5789 * np.log(10**x) - 1.83) + 0.4192
            y_pathway = 0.2589 * np.arctan(-0.5789 * np.log(x) - 1.83) + 0.4192
            # mechanical injury
            # y_mechanical = 0.345 * np.arctan(-0.2923 * np.log(10**x) - 0.1617) + 0.5033
            y_mechanical = 0.345 * np.arctan(-0.2923 * np.log(x) - 0.1617) + 0.5033

            g.ax_joint.plot(
                x,
                y_pathway,
                linestyle="--",
                color="green",
                linewidth=2,
                alpha=0.8,
                label="pathway induced injury",
            )
            # g.ax_joint.legend()
            g.ax_joint.legend(loc="upper right")

        if INJURY_1:
            # y_cell_death = 0.128 * x ** (-0.156)
            y_cell_death = cell_death_strain_rate_to_strain(x)

            g.ax_joint.plot(
                x,
                y_cell_death,
                linestyle="--",
                color="black",
                linewidth=2,
                alpha=0.8,
                label="cell death",
            )
            g.ax_joint.legend(loc="upper right")

            x_intercept = probes["strain_rate_p95"][idx]  # strain rate 10^x
            y_intercept = cell_death_strain_rate_to_strain(x_intercept)  # strain
            y_intercept_txt = "{:.{}f}".format(
                y_intercept, 4
            )  # 0.0767 trans, 0.0990 for rot
            x_offset = 0  # strain rate
            y_offset = 0.005  # strain

            # strain_rate_txt = r" 95\% = " + str(round(strain_rate_095th, 1))
            # intercept_txt = f"( {x_intercept}, {y_intercept})"
            intercept_txt = "(" + strain_rate_txt + ", " + y_intercept_txt + ")"
            # intercept_txt = "(x, y)"
            # g.ax_joint.text(0.02, -0.015, axis_txt, ha="left", va="bottom", bbox=bbox_props)
            # g.ax_joint.annotate(
            #     intercept_txt,
            #     xy=(x_intercept, y_intercept),
            #     xycoords="data",
            #     xytext=(x_intercept + x_offset, y_intercept + y_offset),
            # )
            intercept_label_x = time_label_x  # strain rate
            intercept_label_y = 0.08  # strain
            g.ax_joint.annotate(
                intercept_txt,
                xy=(x_intercept, y_intercept),
                xycoords="data",
                xytext=(
                    intercept_label_x + x_offset,
                    intercept_label_y + y_offset,
                ),
                # arrowprops=dict(facecolor="black", arrowstyle="->"),
                arrowprops=dict(facecolor="black", arrowstyle="simple"),
                horizontalalignment="left",
                verticalalignment="top",
            )

    plt.show()

if SERIALIZE:
    title_string = FIG_NAME + "_" + axis_txt + "." + FIG_FORMAT
    g.savefig(title_string, dpi=DPI, bbox_inches="tight")  # avoid cutoff of labels
    print("Figure was saved to: " + os.path.join(os.getcwd(), title_string))


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
