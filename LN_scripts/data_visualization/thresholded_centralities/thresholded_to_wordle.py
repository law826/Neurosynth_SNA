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
			'graph_stats/visualizations/'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Thresholds for graphs.
thresholds = [x/10 for x in range(10)]

for threshold in thresholds:
	thresh_graph = ns.ThresholdGraph(graph, threshold)

	# Calculate centralities.
	node_names = graph.vs['term']
	degree_cent = graph.strength(loops=False, weights='weight')
	betweenness_cent = graph.betweenness(directed=False, 
						weights='weight')
	eigenvector_cent = graph.evcent(directed=False, weights='weight')
	closeness_cent = graph.closeness(weights='weight')

	centralities = [degree_cent, betweenness_cent, 
	eigenvector_cent, closeness_cent]

	for centrality in centrality:
		
		with open()




import pdb; pdb.set_trace()



# wordle_text_generator(terms, weights, outpath)

