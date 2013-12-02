#!/bin/python

"""
This will import an edgelist and save the relevant pickle.
The graph will be undirected.
Node attributes will be added.
Attach number of studies.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
try:
	from igraph import *
except ImportError:
	raise ImportError, "The igraph module is required to run this program."
import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc

edgelist = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'NeurosynthMerge/merged_edgelist/merged_edgelist.csv'


outpath = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

# Import the graph from an edgelist.
graph = ns.ImportNcol(edgelist)

# Make graph undirected.
graph.to_undirected(mode="collapse", combine_edges= "max")

# Strip loops from the graph.
graph = db.StripLoops(graph)

# Add term names.
neurosynth_dir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/neurosynthgit/' \
			'results/run2/Reverse_Inference2/'

raw_terms = ns.GetFileNamesInDirectory(neurosynth_dir)
graph = ns.StripName(graph, raw_terms)

### Add number of studies.
lc = lc.ListClass()

# All terms in the graph.
nodes = graph.vs['term'] 

# Tuples of the term to use and the merge expression.
thesaurus_merge_terms = [(x[0], x[-1]) for x in lc.thesaurus]

# Dictionary of the above.
thesaurus_dict = {key: value for (key, value) in thesaurus_merge_terms}

# Total list of merge expressions across all nodes.
total_merge_list = []
for node in nodes:
	if node in thesaurus_dict:
		total_merge_list.append(thesaurus_dict[node])
	else:
		total_merge_list.append(node)

git_path = os.path.join('/Volumes', 'huettel', 'KBE.01', 
			'Analysis', 'Neurosynth', 'neurosynthgit')
aa = ns.ArticleAnalysis(git_path)

num_art = aa.CalculateNumberofArticlesForManyTerms(total_merge_list)

# Manually input number of studies for 1back and 2back due to error in yacc.
num_art[0] = 37
num_art[1] = 84

graph.vs['numberofstudies'] = num_art

import pdb; pdb.set_trace()


# Save the graph.
ns.SaveGraph(graph, outpath)

