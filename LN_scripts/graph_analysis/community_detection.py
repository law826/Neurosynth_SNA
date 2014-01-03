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

# Load the graph.
graph = ns.LoadGraph(graph_pth)

def vc_to_textfile(vc_object, outdir, outputname):
	# Output a text file for the general graph.
	outpath = os.path.join(outdir, outputname)
	with open(outpath, 'wb') as outfile:
		for cluster in range(max(vc_object.membership)):
			outfile.write('Cluster number %.0f\n' %(cluster))
			nodes_of_cluster = [graph.vs['term'][i] 
								for i, node in enumerate(vc_object.membership)
								if node == cluster]
			for node_of_cluster in nodes_of_cluster:
				outfile.write('%s\n' % node_of_cluster)
			outfile.write('\n\n')

def fast_greedy(graph, threshold, outputname):
	"""
	Takes a graph, threshold, and name of outputname, and outputs a text file
	of the relevant clusters.
	"""
	# Threshold the graph.
	graph = ns.ThresholdGraph(graph, threshold)

	# Fast greedy community detection.
	vd_object = graph.community_fastgreedy(weights='weight')
	vc_object = vd_object.as_clustering(vd_object.optimal_count)

	# Output to text file.
	vc_to_textfile(vc_object, outdir, outputname)

def community_multilevel(graph,threshold,outputname):
	"""
	Takes a graph, threshold, and name of outputname, and outputs a text file
	of the relevant clusters.
	"""
	graph = ns.ThresholdGraph(graph, threshold)

	# Community_multilevel algorithm.
	vc_object = graph.community_multilevel(weights='weight')

	# Output to text file.
	vc_to_textfile(vc_object, outdir, outputname)

def community_edge_betweenness(graph, threshold, outputname):
	"""
	Same as above with community edge betweenness. This may be more analogous
	to 
	"""
	graph = ns.ThresholdGraph(graph, threshold)

	# Community betweenness algorithm.
	vd_object = graph.community_edge_betweenness(directed=False, weights='weight')
	vc_object = vd_object.as_clustering(vd_object.optimal_count)

	# Output to text file.
	vc_to_textfile(vc_object, outdir, outputname)

if __name__ == '__main__':
	#fast_greedy(graph, 0.5, 'clusters_fastgreedy_05.txt')
	#community_multilevel(graph, 0.6, 'clusters_community_multilevel_06.txt')
	community_edge_betweenness(graph, 0.1, 'clusters_community_edge_betweenness_01.txt')

	try:
		os.system(
			"""osascript -e 'tell app "System Events" to display""" \
			""" dialog "Your script has finished running."'""")
	except:
		pass


# Output a text file with singleton clusters removed. 
# Delete singletons: ability, animal, association, discrimination, error, 
# image, manipulation, mask, order, perceived, response, search, selection,
# space, taskrelated, time, topdown




