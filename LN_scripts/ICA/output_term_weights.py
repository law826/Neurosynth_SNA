"""
Output term weights.
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
import ListClass as lc

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/radar_plots')
import single_panel_radar
import csv

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
from shuffle_functions import get_shuffled_terms

def output_term_weights(terms, ICA_path):
	"""
	Makes a csv with the term weights which serves as input for several other
	scripts.
	"""
	all_data = [] 
	for term in terms:
		data = single_panel_radar.get_sorted_list_by_term(term, ICA_path, sort_list = False)
		data_row = [datum[1] for datum in data]
		data_row.insert(0, term)
		all_data.append(data_row)

	# Write to csv.
	# Tranpose the lists.
	csv_list = [list(row) for row in zip(*all_data)]
	with open(os.path.join(distribution, 'term_weights.csv'), 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(csv_list)


def igraph_matched(graph_pth, ICA_path):
	"""
	Takes terms from an igraph and assigns that the weight csv. 
	"""
	graph = ns.LoadGraph(graph_pth)
	terms = graph.vs['term']
	output_term_weights(terms, ICA_path)

def shuffled_run(shuffle_log_path, ICA_path):
	"""
	Take terms from a log file.
	"""
	terms = get_shuffled_terms(shuffle_log_path)
	output_term_weights(terms, ICA_path)


if __name__ == '__main__':
	graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'
	ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/old/SHUFFLED3/'
	distribution = os.path.join(ICA_path, 'distribution')
	shuffle_log_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/'\
			'neurosynthgit/results/run2/merged_images_ri/shuffled_log.txt'

	shuffled_run(shuffle_log_path, ICA_path)