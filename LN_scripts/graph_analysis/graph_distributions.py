#!/usr/bin/evn python

"""
Produces graphs of various node measures.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
import pylab as P

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc


graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

outdir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'graph_stats/visualizations/'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

histogram_of_zero_order_correlation = False
histogram_of_number_of_studies = False
histogram_of_number_of_studies_lower_range = False
histogram_of_partial_correlations = True

if histogram_of_zero_order_correlation:
	P.figure()
	x = graph.es['weight']
	import pdb; pdb.set_trace()
	histogram = P.hist(x)
	P.xlabel('Pearson Correlation (R)')
	P.ylabel('Number of Edges')
	P.savefig(os.path.join(outdir, 'edge_weight_histogram'))

if histogram_of_number_of_studies:
	P.figure()
	y = graph.vs['numberofstudies']
	stud_histogram = P.hist(y, bins=100)
	P.xlabel('Number of Studies')
	P.ylabel('Number of Nodes')
	P.savefig(os.path.join(outdir, 'num_studies_histogram'))

if histogram_of_number_of_studies_lower_range:
	P.figure()
	y = graph.vs['numberofstudies']
	stud_histogram = P.hist(y, bins=10, range=(0, 1000))
	P.xlabel('Number of Studies')
	P.ylabel('Number of Nodes')
	P.savefig(os.path.join(outdir, 'num_studies_histogram_lower_range'))

if histogram_of_partial_correlations:
	P.figure()
	x = graph.es['partialcorrelation']
	histogram = P.hist(x, bins=100, range=(-0.2, 0.2))
	P.xlabel('Partial Correlation')
	P.ylabel('Number of Edges')
	P.savefig(os.path.join(outdir, 'partial_correlation_edges'))