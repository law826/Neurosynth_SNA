"""
Given an ICA run, calculates the Gini coefficient for each term in Neurosynth.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
import glob
import csv

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/Gini/')
import utilities

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
import ICA_data_visualization as idv

# Get terms.
graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'
graph = ns.LoadGraph(graph_pth)
terms = graph.vs['term']

# ICA path.
ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'

outpath = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/distribution/'

## Get all relevant weights for each term.
data = []
data.append(['term', 'sum', 'std', 'max', 'min', 'gini_min', 'gini_pos'])
for term in terms:
	term_data = idv.get_sorted_list_by_term(term, ICA_path)
	weights = [item[1] for item in term_data]

	# Calculate ginis.
	# Based on subtraction of the minimum.
	minimum = min(weights)
	g_weights = [weight-minimum for weight in weights]
	gini_min = utilities.calc_gini(g_weights)

	# Look only at positive numbers. 
	g_weights = [weight for weight in weights if weight > 0]
	gini_positive = utilities.calc_gini(g_weights)

	weights = np.array(weights)

	#Calculate various other metrics of interest.
	sum_of_weights = np.sum(weights)
	std_of_weights = np.std(weights)
	max_of_weights = np.amax(weights)
	min_of_weights = np.amin(weights) 
	data.append([term, np.sum(weights), np.std(weights), 
		np.amax(weights), np.amin(weights), gini_min, gini_positive])

# Write to csv.
with open(os.path.join(outpath, 'gini_data.csv'), 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(data)

	# # Calculate the Gini coefficient.
	# x = [term_datum[1] for term_datum in term_data]

	# # All of the formulas from utilies for gini yield the same result.
	# gini = utilities.calc_gini(x)
	# ginis.append((term, gini))
	# print ginis[-1]

sys.path.append('/Users/ln30/Git/general_scripts/')
import send_message; send_message.send_text()
import pdb; pdb.set_trace()