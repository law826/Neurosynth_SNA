#!/bin/python

"""
This will import an edgelist and save the relevant pickle.
"""

from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
try:
	from igraph import *
except ImportError:
	raise ImportError, "The igraph module is required to run this program."
import igraph

#sys.path.append(os.path.realpath('..'))
sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns

edgelist = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'NeurosynthMerge/merged_edgelist/merged_edgelist.csv'


outpath = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'


graph = ns.ImportNcol(edgelist)

ns.SaveGraph(graph, outpath)


import pdb; pdb.set_trace()