# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
import scipy.odr
import numpy

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

csv_output = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
		'graph_analysis_data/graph_stats/merged_centrality/centralities.csv'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

correlations = graph.es['weight']
jaccards = graph.es['jaccards']

# Filter NaNs and convert to numpy arrays.
cj = zip(correlations, jaccards)
indices_to_delete = [i for i, pair in enumerate(cj) if pair[1] == 'NA']
edge_labels = [graph.vs[edge.tuple[0]]['term'] + ' ' + graph.vs[edge.tuple[1]]['term']
				for edge in graph.es]
graph.delete_edges(indices_to_delete)
cj = [(pair[0], pair[1], i) for i, pair in enumerate(cj) if pair[1] != 'NA']

correlations = numpy.asarray([pair[0] for pair in cj])
jaccards = numpy.asarray([pair[1] for pair in cj])

def f(B, x):
	return B[0]*x + B[1]

def odr(f):
	linear = scipy.odr.Model(f)
	odr_data = scipy.odr.RealData(correlations, jaccards)
	odr_model = scipy.odr.ODR(odr_data, linear, beta0=[0,0])
	odr_out = odr_model.run()
	odr_slope, odr_intercept = odr_out.beta
	odr_predY = odr_slope*correlations + odr_intercept
	odr_predX = (1./odr_slope)*jaccards - (odr_intercept/odr_slope)
	odr_theta = numpy.arctan((odr_predX-correlations)/(odr_predY-jaccards))
	odr_distances = (odr_predY-jaccards) * numpy.sin(odr_theta)

	booleanY = jaccards > odr_predY
	booleanX = correlations > odr_predX
	distance_tuples = zip(edge_labels, odr_distances, booleanX, booleanY)
	sorted_distances = sorted(distance_tuples, 
						key=lambda component: component[1], reverse = True)

	top_correlations = [tup for tup in sorted_distances if tup[2] == True]
	top_jaccards = [tup for tup in sorted_distances if tup[3]==True]

	import pdb; pdb.set_trace()





if __name__ == '__main__':
	odr(f)