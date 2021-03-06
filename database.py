from __future__ import division
import os
import sys
import random as rand
import cPickle 
import numpy as np
import getpass
#import nltk
from pdb import *
from igraph import *
import pickle

# import basefunctions
#import tkMessageBox
#import tkFileDialog
#import tkentrycomplete as tkcomp
#import re
#from Tkinter import *
#import basefunctions as bf

"""
[] Complete merge functionality
"""

def AddNode(nodename, type, graph=None):
	"""
	Takes: (1) the name of the node (attribute='term') (2) the type (attribute='type') (3) an optional graph.

	- Adds a new node and creates a new graph if no graph is provided. 
	- It does not do anything if the node name already exists.

	Returns: (1) updated graph (2) node index.
	"""
	if graph == None:
		graph = Graph()
		graph.add_vertices(1)
		graph.es["weight"] = 1.0
		graph["name"] = "Ideas Graph"			
		graph.vs[0]["name"] = nodename
		graph.vs[0]["type"] = type
		node_index = 0
	else:
		try:
			"""
			If node already exists, then don't add a new node.
			"""
			node_index = graph.vs.find(name=nodename).index
		except ValueError:
			"""
			Add a node if the node does not already exist.
			"""
			graph.add_vertices(1)
			number_of_vertices = graph.vcount()
			graph.vs[number_of_vertices-1]["name"] = nodename
			graph.vs[number_of_vertices-1]["type"] = type
			node_index = number_of_vertices-1 #This is the node's index.
	
	return graph, node_index
			
def AddAllEdges(graph, node_index_list):
	"""
	Takes: (1) a graph (2) a list of all relevant node indices.

	Add combinations of all possible edges for a group of nodes while 
	preventing the formation of multiples and loops.

	Returns: updated graph. 
	"""
	for first_index_counter, first_vertex in enumerate(node_index_list):
		for second_vertex_counter in range((len(node_index_list)-1)):
			second_index = first_index_counter+second_vertex_counter+1
			if second_index <= (len(node_index_list)-1):
				second_vertex = node_index_list[second_index]

				# Only add edge if edge doesn't exist (prevent multiples) and prevent forming loops:
				if first_vertex != second_vertex:
					try:
						graph.get_eid(first_vertex, second_vertex)
					except InternalError:
						graph.add_edges((first_vertex, second_vertex))
	
	return graph

def IdentifySimilarNodes(inlist, threshold=0.25):
	"""
	Takes: (1) takes a list of the names of nodes (2) optional threshold for
	Levenshtein distance (normalized by the sum of the number of letters in a pair) - 
	smaller threshold means more stringent.

	Returns: (1) a list of unique list of tuples of similar nodenames. 
	"""
	tuple_combos = [(x,y) for x in inlist for y in inlist if x!=y]
	similar_nodes_tuples = []
	for entry in tuple_combos:
		if (entry[1], entry[0]) in tuple_combos:
			tuple_combos.remove((entry[1], entry[0])) 

		total_length = len(entry[0]) + len(entry[0])
		normed_LD = (nltk.metrics.edit_distance(*entry))/total_length

		if normed_LD < threshold:
			similar_nodes_tuples.append(entry)

	return similar_nodes_tuples

def MergeNodes(graph, nodename1, nodename2):
	"""
	Takes: (1) graph (2) name of first node (3) name of second node

	Merge two nodes such that node1 is the remaining node and inherits all of the edges of node 2.

	Returns: an updated graph.
	"""

	# Find neighbors of node 2.
	pre_everyone = [node.index for node in graph.vs.find(name=nodename2).neighbors()]
	everyone = pre_everyone + [graph.vs.find(name=nodename1).index]
	
	# Make edges from node 2 to node 1.
	AddAllEdges(graph, everyone)

	# Delete node 2.
	graph.delete_vertices(graph.vs.find(name=nodename2).index)

def MergeWeightedNodes(graph, nodename1, nodename2):
	"""
	Similar to MergeNodes except for weighted edges such that the new node retains the highest weighted edges.
	"""

	# Find neighbors of node 2.
	everyone_name = [node['name'] for node in graph.vs.find(name=nodename2).neighbors()]

	for neighbor in everyone_name:
		try:
			graph[nodename1, neighbor]
			if graph[nodename1, neighbor] >= graph[nodename2, neighbor]:
				pass
			else:
				graph[nodename1, neighbor] = graph[nodename2, neighbor]
		except ValueError:
			graph[nodename1, neighbor] = graph[nodename2, neighbor]

	# Delete node 2.
	graph.delete_vertices(graph.vs.find(name=nodename2).index)

	return graph

def DocumentMergedPair(nodename1, nodename2, save_file):
	"""
	Given two nodes, this will save the pair in a list of tuples in either a new file (if file doesn't exist) 
	or in the file given.
	"""
	try:
		merged_pairs = pickle.load(open(save_file, 'rb'))
	except IOError:
		merged_pairs = []
	merged_pairs.append((nodename1, nodename2))
	pickle.dump(merged_pairs, open(save_file, 'wb'))

def IsolateSubGraph(graph, nodename_list, attribute_name):
	"""
	Takes: (1) graph (2) list of names of nodes that should be matched. (3) name of the attribute that corresponds to nodename_list.

	This will keep the interconnections between those members on the list, but ignore edges and nodes not in the list.

	Returns: (1) a new subgraph
	"""
	node_list = []
	for nodename in nodename_list:
		kwargs = {}
		kwargs[attribute_name] = nodename
		try:
			node_list.append(graph.vs.find(**kwargs))
		except ValueError:
			pass

	sub_graph = graph.subgraph(node_list)
	return sub_graph

def NodesInOrderOfCentrality(graph, type):
	"""
	Takes: (1) graph (2) type of centrality desired.
	Returns: A list of tuples of node name and centrality statistic.
	"""
	if type == 'degree':
		pre_list_of_tuples = [(node["term"], node.strength(loops=False, weights="weight")) for node in graph.vs]

	elif type == 'betweenness':
		pre_list_of_tuples = [(node["term"], node.betweenness(directed=False, weights="weight")) for node in graph.vs]

	elif type == 'eigenvector':
		ec = graph.eigenvector_centrality(weights="weight")	
		pre_list_of_tuples = [(nodeterm, ec[i]) for i, nodeterm in enumerate(graph.vs["term"])]

	elif type == 'closeness':
		pre_list_of_tuples = [(node["term"], node.closeness(weights="weight")) for node in graph.vs]


	# The following were used to sort the items in order. 
	# list_of_tuples = sorted(pre_list_of_tuples, key=lambda pair: pair[1])
	# list_of_tuples.reverse()

	return pre_list_of_tuples

def StripLoops(graph):
	try:
		index_to_delete = [i for i, x in enumerate(graph.is_loop()) if x]
		graph.delete_edges(index_to_delete)
	except IndexError:
		pass
	return graph
