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
			'graph_stats/graph_distributions/'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Histogram of the edge weights.
P.figure()
x = graph.es['weight']
histogram = P.hist(x)
P.xlabel('Pearson Correlation (R)')
P.ylabel('Number of Edges')
P.savefig(os.path.join(outdir, 'edge_weight_histogram'))

# Graph a histogram of the number of studies.
P.figure()
y = graph.vs['numberofstudies']
stud_histogram = P.hist(y, bins=100)
P.xlabel('Number of Studies')
P.ylabel('Number of Nodes')
P.savefig(os.path.join(outdir, 'num_studies_histogram'))

# Lower extent of the above
P.figure()
y = graph.vs['numberofstudies']
stud_histogram = P.hist(y, bins=10, range=(0, 1000))
P.xlabel('Number of Studies')
P.ylabel('Number of Nodes')

P.savefig(os.path.join(outdir, 'num_studies_histogram_lower_range'))

import pdb; pdb.set_trace()