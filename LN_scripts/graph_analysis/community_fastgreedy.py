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

outdir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/'\
			'graph_stats/clustering/'


make_text_file = True
make_collapsed_subgraph = False

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Threshold the graph.
graph = ns.ThresholdGraph(graph, 0.5)

# Invert the edges?

# Fast greedy community detection.
vd_object = graph.community_fastgreedy(weights='weight')
vc_object = vd_object.as_clustering(vd_object.optimal_count)

# Membership of all the nodes.
vc_object.membership

# Output a text file for the general graph.
if make_text_file:
	outpath = os.path.join(outdir, 'clusters_louvain_05.txt')
	with open(outpath, 'wb') as outfile:
		for cluster in range(max(vc_object.membership)):
			outfile.write('Cluster number %.0f\n' %(cluster))
			nodes_of_cluster = [graph.vs['term'][i] 
								for i, node in enumerate(vc_object.membership)
								if node == cluster]
			for node_of_cluster in nodes_of_cluster:
				outfile.write('%s\n' % node_of_cluster)
			outfile.write('\n\n')

# Output a text file with singleton clusters removed. 
# Delete singletons: ability, animal, association, discrimination, error, 
# image, manipulation, mask, order, perceived, response, search, selection,
# space, taskrelated, time, topdown




