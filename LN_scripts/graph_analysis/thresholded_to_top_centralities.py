"""
Threshold a graph and create a wordle visualization.
"""
# Set up.
from __future__ import division
import os, sys, getpass, random as rand, cPickle, numpy as np, csv
import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc


sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/data_visualization/')
from wordle_visualization import wordle_text_generator

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/'\
			'pickles/reverse_graph2.p'

outdir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/'\
			'graph_stats/visualizations/wordle'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Thresholds for graphs.
thresholds = [x/10 for x in range(10)]

# All the node names which don't need to be looped. 
node_names = np.array(graph.vs['term'])

# Make empty arrays
degree_overall = np.empty((414, 10))
eigenvector_overall = np.empty((414, 10))
closeness_overall = np.empty((414, 10)) 
betweenness_overall = np.empty((414, 10)) 

for i, threshold in enumerate(thresholds):
	thresh_graph = ns.ThresholdGraph(graph, threshold)

	# Calculate centralities and make the numpy arrays.
	degree_cents = np.array(graph.strength(loops=False, weights='weight'))
	eigenvector_cents = np.array(graph.evcent(directed=False, weights='weight'))
	closeness_cents = np.array(graph.closeness(weights='weight'))

	# Fix edges so that betweenness works.
	graph.es['weight_adj'] = [2-x for x in graph.es['weight']]
	betweenness_cents = np.array(graph.betweenness(directed=False, 
						weights='weight_adj'))
	centralities = [degree_overall, betweenness_overall, 
	eigenvector_overall, closeness_overall]
	centrality_names = ['degree', 'betweenness', 'eigenvector', 'closeness']

	# Insert relevant columns.
	degree_overall[:,i] = degree_cents
	eigenvector_overall[:,i] = eigenvector_cents
	closeness_overall[:,i] = closeness_cents 
	betweenness_overall[:,i] = betweenness_cents 

# Make matrix with all thresholds for each type of centrality.
for i, centrality in enumerate(centralities):
	outpath = os.path.join(outdir, '%s.csv' %(centrality_names[i]))
	np.savetxt(outpath, centrality, fmt='%.3f', delimiter = ',')