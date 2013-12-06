"""
Loads a graph and outputs a csv with the appropriate centralities.
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

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

csv_output = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
		'graph_analysis_data/graph_stats/merged_centrality/pcentralities.csv'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Add constant to weights to allow for proper centrality calculation.
graph.es['partialcorrelation'] = [x+2 for x in graph.es['partialcorrelation']]

# Calculate centralities.
node_names = graph.vs['term']
degree_cent = graph.strength(loops=False, 
				weights='partialcorrelation')
betweenness_cent = graph.betweenness(directed=False,
				weights='partialcorrelation')

# Write to a csv.
with open(csv_output, 'wb') as output:
	for i, node in enumerate(graph.vs):	
		output.write(
			'%s, %s, %s\n' %(node_names[i], degree_cent[i],
				betweenness_cent[i]))