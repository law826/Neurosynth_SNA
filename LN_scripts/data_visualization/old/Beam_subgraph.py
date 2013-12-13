"""
Produces a subgraph that corresponds to Beam et al.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
from igraph import *

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


listclass = lc.ListClass()
sub_list_concept = listclass.sub_Beam_concepts
ns = graph.vs['numberofstudies']
#creates attribute for number of studies
npns = np.array(ns) #creates array of number of studies
nsl = np.log10(npns) #calculates log of number of studies
graph.vs["log"] = nsl*8 #multiplies constant to create attribute "log"



subgraph = db.IsolateSubGraph(graph, sub_list_concept, "term") 
# creates sub graph from main graph rg

index_to_delete = [edge.index for edge in subgraph.es.select(weight_lt=0.2)] 
# creates threshold by selecting edges lower than a certain weight

subgraph.delete_edges(index_to_delete) #deletes selected edges
visual_style = {} #sets method of modifying graph characteristics
visual_style ["vertex_label"]= subgraph.vs["term"] # labels the vertices
visual_style ["vertex_label_dist"] = 1.0 
# specifies the distance between the labels and the vertice
visual_style ["vertex_size"] = subgraph.vs["log"] 
# specifies size of vertex_size
visual_style["bbox"] = (750,750) #sets dimensions for the box layout
visual_style ["margin"] = 60
plot(subgraph, **visual_style) # creates the changes