import os

import numpy as np; np.random.seed(0)
# import pandas as pd
import seaborn as sns; sns.set(style="white", color_codes=True)
import matplotlib.pyplot as plt
from matplotlib import rc

EXEMPLAR = 0  # turn on or off the exemplar problem
FIG_NAME = os.path.basename(__file__).split('.')[0]  # remove the .py extension
FIG_FORMAT = 'pdf'
LATEX = 1
SERIALIZE = 1  # turn on or off write figure to disk

# sns.axes_style("darkgrid")
sns.set(style="darkgrid")
bbox_props = dict(boxstyle='square, pad=0.2', fc='white', ec='black', lw=1)

if LATEX:
    #rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
    rc('text', usetex=True)
    rc('font', family='serif')


## Exemplar joint distribution plot - begin
if EXEMPLAR: 
    tips = sns.load_dataset("tips")

    tip_data = np.array(tips["tip"])
    bill_data = np.array(tips["total_bill"])

    # legend_txt = 'hello'
    # legend_properties = {'weight': 'bold', 'size': 12}

    g = sns.JointGrid(bill_data, tip_data)
    # g = g.plot_joint(plt.scatter, s=10, linewidths=0.05, edgecolors='blue', marker='o', alpha=0.3, label=legend_txt)
    g = g.plot_joint(plt.scatter, s=10, linewidths=0.05, edgecolors='blue', marker='o', alpha=0.3)

    _ = g.ax_marg_x.hist(bill_data, color="b", bins=np.arange(0,60,5))
    _ = g.ax_marg_y.hist(tip_data, color="g", orientation="horizontal", bins=np.arange(0,12,1))
    # _ = g.ax_joint.legend(prop=legend_properties, loc='upper left')
    _ = g.ax_joint.text(20, 10, 'hello', ha='left', va='bottom', bbox=bbox_props)

    plt.xlabel("total bill")
    plt.ylabel("tip")

    plt.show()
    ## Exemplar joint distribution plot - end

else:
    
    ## -------------------------------- ##
    ## Client application initializaton - begin
    script_pth = os.getcwd()
    
    ## Client application initializaton - end
    ## -------------------------------- ##
    
    
    ## -------------------------------- ##
    ## User Input Deck, simulation-specific input - begin
    
    # block 7 is white matter is 504,505 data points 
    # block 8 is gray matter is 790,102 data points
    # combined white + gray = 1,294,607 data points
    
    # relative to this script, location of the particular simulation
    simulation_path = '../../../casco_sim/bob-1mm-5kg-helmet2-0305-hemi-063f/'

    # time_steps = [30, 51, 57]
    # times = [0.0058, 0.010, 0.0112] # seconds
    idx = 0  # index for the probes
    probes = {
        "steps": [30, 51, 57],
        "time": [0.00580000428262166, 0.010000030740917116, 0.011200009903610695],
        "strain_p95": [0.013038920686082887, 0.007864328738051788,0.009356105757136385],
        "strain_rate_p95": [26.62451150429535, 45.64035758617126, 47.167653798895905]
    }

    axis_txt = f'time = {probes["time"][idx]*1000:.3f} ms (Bob-063f)'
    # strain_rate_txt = f'95% = {probes["strain_rate_p95"][idx]:.2f} /s' 
    # strain_txt = f'95% = {probes["strain_p95"][idx]:.3f}'

    blocks = [7, 8]
    labels = ['white matter','gray matter']
    colors = ['C1','C2']  # white plotted as orange, gray -> green
    # strain_files = [
    #     'ts_30_block_7_max_principal_green_lagrange_strain.txt','ts_30_block_8_max_principal_green_lagrange_strain.txt']
    strain_files = [
        [
            'ts_30_block_7_max_principal_green_lagrange_strain.txt',
            'ts_30_block_8_max_principal_green_lagrange_strain.txt'
        ],[
            'ts_51_block_7_max_principal_green_lagrange_strain.txt',
            'ts_51_block_8_max_principal_green_lagrange_strain.txt'
        ],[
            'ts_57_block_7_max_principal_green_lagrange_strain.txt',
            'ts_57_block_8_max_principal_green_lagrange_strain.txt'
        ]
    ]

    strain_rate_files = [
        [
            'ts_30_block_7_max_principal_green_lagrange_strain_rate.txt',
            'ts_30_block_8_max_principal_green_lagrange_strain_rate.txt'
        ],[
            'ts_51_block_7_max_principal_green_lagrange_strain_rate.txt',
            'ts_51_block_8_max_principal_green_lagrange_strain_rate.txt'
        ],[
            'ts_57_block_7_max_principal_green_lagrange_strain_rate.txt',
            'ts_57_block_8_max_principal_green_lagrange_strain_rate.txt'
        ]
    ]

    ## User Input Deck, simulation-specific input - end
    ## -------------------------------- ##
    

    # fig, ax = plt.subplots(figsize=(8,8))
    # ax.set_aspect("equal")
    strain = np.array([])
    strain_rate = np.array([])

    # for i, (s, sr) in enumerate(zip(strain_files, strain_rate_files)):
    for s, sr in zip(strain_files[idx], strain_rate_files[idx]):  # collect over all blocks

        block_strain = np.genfromtxt(os.path.join(simulation_path, s))
        block_strain_rate = np.genfromtxt(os.path.join(simulation_path, sr))
        strain = np.concatenate((strain, block_strain))
        strain_rate = np.concatenate((strain_rate,  block_strain_rate))
    
    g = sns.JointGrid(strain_rate, strain)
    g = g.plot_joint(plt.plot, linestyle='', marker=',', markersize=0.7, alpha=0.2)

    exp_min = -1  # x-domain minimum 10^exp_min
    exp_max = 3  # x-domain maximum 10^exp_max
    npts = 24  # number of points

    strain_rate_095th = np.percentile(strain_rate, 95.0)  # 95th percentile strain rate
    x_bins = np.logspace(exp_min, exp_max, 2*npts)
    _ = g.ax_marg_x.hist(strain_rate, bins=x_bins)

    strain_095th = np.percentile(strain, 95.0)  # 95th percentile strain
    strain_min = np.amin(strain)
    strain_max = np.amax(strain)
    y_bins = np.linspace(strain_min, strain_max, npts)
    _ = g.ax_marg_y.hist(strain, orientation="horizontal", bins=y_bins)

    g.ax_joint.set_xscale('log')
    g.ax_marg_x.set_xscale('log')
    g.ax_joint.set_xlim([0.01, 10000])
    # g.ax_joint.set_xlim([10**exp_min, 10**exp_max])
    g.ax_joint.set_ylim([-0.02, 0.10])

    g.ax_joint.text(0.02, 0.09, axis_txt, ha='left', va='bottom', bbox=bbox_props)

    # draw 95th percentile boundaries
    line_prop = dict(color='orange', linewidth=1)
    # vertical line on joint plot
    g.ax_joint.plot([strain_rate_095th, strain_rate_095th], g.ax_joint.get_ylim(), **line_prop)

    # horizontal line on the joint plot
    g.ax_joint.plot(g.ax_joint.get_xlim(), [strain_095th, strain_095th], **line_prop)

    # vertical line across marginal strain rate plot
    y0_log_sr, y1_log_sr = g.ax_marg_x.get_ylim()
    g.ax_marg_x.plot([strain_rate_095th, strain_rate_095th], [y0_log_sr, y1_log_sr], **line_prop)
    # marginal strain rate text
    strain_rate_txt = r' 95\% = ' + str(round(strain_rate_095th, 1))
    # g.ax_marg_x.text(strain_rate_095th, (y0_log_sr + y1_log_sr) / 2.0, ' 95% = ' + str(round(strain_rate_095th, 1)), ha='left', va='bottom')
    g.ax_marg_x.text(strain_rate_095th, (y0_log_sr + y1_log_sr) / 2.0, strain_rate_txt, ha='left', va='bottom')

    # horizontal line on the marginal strain plot
    x0_strain, x1_strain = g.ax_marg_y.get_xlim()
    g.ax_marg_y.plot([x0_strain, x1_strain], [strain_095th, strain_095th], **line_prop)
    # marginal strain text
    strain_txt = r'95\% = ' + str(round(strain_095th, 4))
    g.ax_marg_y.text((x0_strain + x1_strain)/ 2.0, strain_095th, strain_txt, ha='center', va='bottom')


    g.ax_joint.grid(color='gray')
    g.ax_marg_x.grid(color='gray', axis='x')
    g.ax_marg_y.grid(color='gray', axis='y')

    plt.xlabel("max(eig(GL strain rate)) (1/s)")
    plt.ylabel("max(eig(GL strain)) (cm/cm)")

    plt.show()

if SERIALIZE:
    title_string = FIG_NAME + '_' + axis_txt + '.' + FIG_FORMAT
    g.savefig(title_string, dpi=100)
    print('Figure was saved to: ' + os.path.join(os.getcwd(), title_string))