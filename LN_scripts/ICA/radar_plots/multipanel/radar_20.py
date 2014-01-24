"""
Plot a 20 vertex radar plot.
"""
import os, sys, glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

from base_plot import *

def get_term_weight(term, ICA_path):
    """
    Get a sorted list given a term and ICA_path. Several other pieces of 
    information are included as well.
    """
    # Search a directory for all lines that include a certain term.
    load_dir = os.path.join(ICA_path, 'loadings')
    component_files = glob.glob1(load_dir, "*.txt")

    # Collect all of these into tuples, which includes the component name.
    inter_line_list = [] 
    for component_file in component_files:
        with open(os.path.join(load_dir, component_file), 'rb') as f:
            file_lines = f.readlines()
            for file_line in file_lines:
                if term in file_line: 
                    file_line = file_line.replace('\n', '')
                    intra_line_list = file_line.split(',')
                    # Make sure no nested terms.
                    if intra_line_list[0] == term:
                        intra_line_list[1] = float(intra_line_list[1])
                        numeral_component = component_file.replace('component_', '')
                        numeral_component = numeral_component.replace('.txt', '')
                        intra_line_list.append(int(numeral_component))
                        inter_line_list.append(intra_line_list)

    return inter_line_list

def get_all_term_weights(terms, ICA_path):
    big_list = []
    for term in terms:
        inter_line_list = get_term_weight(term, ICA_path)
        big_list.append(inter_line_list)

    return big_list

def convert_final_data(big_list):
    """
    Make it into a format appropriate for radar plot. 
    This also includes taking the absolute value.
    """
    column_name_list = [str(item[2]) for item in big_list[0]]
    weight_list = [[abs(subitem[1]) for subitem in item] for item in big_list]
    data = {
        'column names': column_name_list,
        'ICA_weights': weight_list
    }

    return data

def overlaid_plot(num_terms, savepath=None):
    ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA%s' %num_terms
    big_list = get_all_term_weights(terms, ICA_path)
    data = convert_final_data(big_list)

    N = num_terms
    theta = radar_factory(N, frame='polygon')

    spoke_labels = data.pop('column names')

    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate axes
    for n, title in enumerate(data.keys()):
        ax = fig.add_subplot(1, 1, n+1, projection='radar')
        #plt.rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(data[title], colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    plt.subplot(1, 1, 1)
    labels = tuple(terms)
    legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
    plt.setp(legend.get_texts(), fontsize='small')

    plt.figtext(0.5, 0.965, 'Differential Term Weightings on ICA components',
                ha='center', color='black', weight='bold', size='large')

    if savepath == None:
        plt.show()
    else:
        plt.savefig(savepath)

if __name__ == '__main__':
    terms = ['reward', 'attention']
    savedir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/visualization/'
    num_terms = 20
    savename = '_'.join(terms)
    savename = '%s_%s' %(savename, num_terms)
    savepath = os.path.join(savedir, savename)

    overlaid_plot(num_terms, savepath=savepath)
    