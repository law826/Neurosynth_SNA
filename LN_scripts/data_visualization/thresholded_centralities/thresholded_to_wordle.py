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

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/data_visualization/')
from wordle_visualization import wordle_text_generator

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Thresholds for graphs.
thresholds = [x/10 for x in range(10)]


# wordle_text_generator(terms, weights, outpath)