#!/bin/python
"""
Take in a CSV generate a text file that can serve as input into Wordle.
Right now, it only takes the second column and multiplies based on 
that count.
"""

import csv
import math

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

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

# Load the graph.
graph = ns.LoadGraph(graph_pth)

def wordle_text_generator(terms, weights, outpath):
	wordle_list = [(x, math.trunc(float(weights[i]))) for i, x in enumerate(terms)]

	# Make a massive concantenated string.
	wordle_string=str()
	for term in wordle_list:
		wordle_string += (term[0]+ ' ') * int(term[1])

	with open(output_text_file, 'w') as text_file:
		text_file.write(wordle_string)


#### Make a list of just all the words as the same size.
terms = graph.vs['terms']
weights = np.ones(len(graph.vs['terms']))
outpath = 

wordle_text_generator(terms, weights, outpath)




##

# # Input file.
# merged_master_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
# 	'graph_analysis_data/graph_stats/merged_graph_master.csv'

# # Output file.
# output_text_file = '/Users/ln30/Git/Neurosynth_SNA/' \
# 	'data_visualization/wordle_string.txt'

# with open(merged_master_path, 'rU') as csvfile:
# 	# Open a CSV object that can be iterated. 
# 	csv_object = csv.reader(csvfile, delimiter=',',
# 		dialect=csv.excel_tab)
# 	# Dump CSV objects items into a python list.
# 	py_list = []
# 	for row in csv_object:
# 		py_list.append(row)

# # Get rid of first row.
# del py_list[0]


# import pdb; pdb.set_trace()

# Refine to a list of just the first and second columns.
# Make the second column a float.
# Add a constant so all numbers all positive.
# Round down the number so that it is an int.
# Amplify the difference for visualization.



