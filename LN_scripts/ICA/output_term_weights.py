"""
Output term weights.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/radar_plots')
import single_panel_plots
import csv

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'
ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'
distribution = os.path.join(ICA_path, 'distribution')


# Load the graph.
graph = ns.LoadGraph(graph_pth)

terms = graph.vs['term']

all_data = [] 
for term in terms:
	data = single_panel_radar.get_sorted_list_by_term(term, ICA_path, sort_list = False)
	data_row = [datum[1] for datum in data]
	data_row.insert(0, term)
	all_data.append(data_row)

# Write to csv.
# Tranpose the lists.
csv_list = [list(row) for row in zip(*all_data)]
f = open(os.path.join(distribution, 'term_weights.csv'), 'wb')
writer = csv.writer(f)
writer.writerows(csv_list)
