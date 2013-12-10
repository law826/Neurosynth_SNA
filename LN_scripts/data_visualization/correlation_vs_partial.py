"""
Makes a hex density plot comparing the zero-order correlations and 
the partial correlations.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
import pylab as plt
import matplotlib.cm as cm
import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import numpy as N
import scipy.odr

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/data_visualization/')
import hexplotting

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

out_pname = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/'\
			'graph_stats/visualizations/corr_vs_pcorr'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

# Get the data
pcorr = graph.es['partialcorrelation']
corr = graph.es['weight']

x = N.array(corr)
y = N.array(pcorr)

hexplotting.Analysis3D(x, y, out_pname)
os.system('open %s.png' % out_pname)