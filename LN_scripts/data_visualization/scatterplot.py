#!usr/bin/env python

"""
Make a scatter plot in matplotlib where all the data points are labeled. 
"""

import numpy as np
import matplotlib.pyplot as plt

def scatter_with_offset_labels(import_file, outpath, labelcol, xcol, ycol,
    labels=True):
    """
    Import file is the csv to draw from.
    labelcol is the column where the labels should be drawn from.
    xcol is the column where the x-axis values should be drawn from.
    ycol is the column where the y-axis values should be drawn from. 
    """

    imported_data = np.genfromtxt(import_file, delimiter=',')
    xbrain = imported_data[:,xcol]
    yjaccard = imported_data[:,ycol]

    with open(import_file, 'r') as f:
        raw = f.readlines()
        labels = []
        for line in raw:
            splitted = line.split(',')
            label = splitted[0]
            labels.append(label)



    plt.subplots_adjust(bottom = 0.1)
    plt.scatter(
        xbrain, yjaccard, marker = 'o', c = "black", 
        cmap = plt.get_cmap('Spectral'))

    # Make alternating labels.

    if labels:
        alternator = 0
        ## x-axis is the brain correlation, y axis is the semantic jaccard.
        for label, x, y in zip(labels, xbrain, yjaccard):
            if alternator == 0:
                xlcoord = -60
                alternator = 1
            elif alternator == 1:
                xlcoord = 100
                alternator = 0
            plt.annotate(
                label, 
                xy = (x, y), xytext = (xlcoord, 20),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', 
                    alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', 
                    connectionstyle = 'arc3,rad=0'), size=7)

    # label = the single label that is assigned to a point.
    # xy = coordinates
    # xytext = coordinates of label
    # ha = horizontal alignment
    # va = vertical alignment

    plt.savefig(outpath)

### Scatter of Degree vs. Betweenness Centrality.

import_file = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
    'graph_analysis_data/graph_stats/merged_centrality/centralities.csv'

outpath = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
    'graph_analysis_data/graph_stats/visualizations/x_degree_y_betweenness'

scatter_with_offset_labels(import_file, outpath, 0, 1, 2, labels=False)