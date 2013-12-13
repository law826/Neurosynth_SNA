"""
Scripts to run create thresholded subgraphs for visualzation.
"""
# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
from ListClass import ListClass

def DrawSubGraph(graph, threshold, sublist_nodes=None):
    """
    Args:
    	graph
        threshold: all edges under this threshold will be deleted.
        sublist_nodes: names of the nodes that should be kept; default is to 
            keep all nodes
    """
    if sublist_nodes != None:
        graph = db.IsolateSubGraph(graph, sublist_nodes, "term") 

    # Delete edges below threshold.
    index_to_delete = [edge.index for edge in graph.es.select(weight_lt=threshold)] 
    graph.delete_edges(index_to_delete) #deletes selected edges


    np_numberofstudies = np.array(graph.vs['numberofstudies']) 
    nsl = np.log10(np_numberofstudies) #calculates log of number of studies
    log_number_of_studies = nsl*8 #multiplies constant to create attribute "log"
    visual_style = {} #sets method of modifying graph characteristics
    visual_style ["vertex_label"] = graph.vs["term"] # labels the vertices
    visual_style ["vertex_label_dist"] = 2 
    # specifies the distance between the labels and the vertices
    visual_style ["vertex_size"] = log_number_of_studies 
    # specifies size of vertex_size
    visual_style["bbox"] = (700,700) #sets dimensions for the box layout
    visual_style["margin"] = 60
    igraph.plot(graph, **visual_style) # creates the changes

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
            'pickles/reverse_graph2.p'

outdir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
            'graph_stats/visualizations/graphs_and_subgraphs/'

# Load the graph.
graph = ns.LoadGraph(graph_pth)
listclass = ListClass()
sublist_nodes = listclass.sub_Beam_concepts


Beam_concepts_020 = False
full_graph = True

if Beam_concepts_020:
    DrawSubGraph(graph, 0.2, sublist_nodes=sublist_nodes)

if full_graph:
    DrawSubGraph(graph, 0.4)

