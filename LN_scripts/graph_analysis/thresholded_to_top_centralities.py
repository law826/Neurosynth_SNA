"""
Threshold a graph and create a wordle visualization.
"""
# Set up.
from __future__ import division
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc


sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/data_visualization/')
from wordle_visualization import wordle_text_generator

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

outdir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/'\
			'graph_stats/visualizations/wordle'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Thresholds for graphs.
thresholds = [x/10 for x in range(10)]

for threshold in thresholds:
	thresh_graph = ns.ThresholdGraph(graph, threshold)

	# Calculate centralities.
	node_names = graph.vs['term']
	degree_cents = graph.strength(loops=False, weights='weight')
	eigenvector_cents = graph.evcent(directed=False, weights='weight')
	closeness_cents = graph.closeness(weights='weight')

	# Fix edges so that betweenness works.
	graph.es['weight_adj'] = [2-x for x in graph.es['weight']]
	betweenness_cents = graph.betweenness(directed=False, 
						weights='weight_adj')

	centralities = [degree_cents, betweenness_cents, 
	eigenvector_cents, closeness_cents]
	centrality_names = ['degree', 'betweenness', 'eigenvector', 'closeness']