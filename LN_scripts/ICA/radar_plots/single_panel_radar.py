"""
Various methods to view the ICA data.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
import glob

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/radar_plots')
import radar_plot
sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
from ICA_utils import descendingLoadings

def get_sorted_list_by_term(term, ICA_path, load_dir, sort_list=True):
	"""
	Get a sorted list given a term and ICA_path. Several other pieces of 
	information are included as well.
	"""
	# Search a directory for all lines that include a certain term.
	component_files = glob.glob1(load_dir, "*.txt")

	# Collect all of these into tuples, which includes the component name.
	inter_line_list = [] 
	for component_file in component_files:
		with open(os.path.join(load_dir, component_file), 'rb') as f:
			file_lines = f.readlines()
			for file_line in file_lines:
				if term in file_line: 
					file_line = file_line.replace('\n', '')
					intra_line_list = file_line.split(',')
					# Make sure no nested terms.
					if intra_line_list[0] == term:
						intra_line_list[1] = float(intra_line_list[1])
						numeral_component = component_file.replace('component_', '')
						numeral_component = numeral_component.replace('.txt', '')
						intra_line_list.append(int(numeral_component))
						intra_line_list.append(component_file)
						inter_line_list.append(intra_line_list)

	# Sort by loadings.
	sorted_inter_line_list = sorted(inter_line_list, key = lambda ill: ill[1],
							reverse = True)

	if sort_list:
		return sorted_inter_line_list
	else:
		return inter_line_list

def radar_plot_top_terms(term, ICA_path, load_dir, dictionary, outpath):
	"""
	Takes the list returned by get_sorted_list_by_term and returns a radar_plot.
	"""
	sorted_inter_line_list = get_sorted_list_by_term(term, ICA_path, load_dir)

	# Retrieve the top 9.
	num_top_items = 15
	num_top_terms = 4
	top_components = sorted_inter_line_list[:num_top_items]

	


	# Retrive the terms to label the radar plot. 
	with open(dictionary_file, 'rb') as df:
		lines = df.readlines()
		# Split because of stupid \r carriage returns. 
		lines = lines[0].split('\r')
		# Make a dictionary. 
		dictionary = {}
		for line in lines:
			line_list = line.split(',')
			# Get rid of empty list items.
			line_list = [item for item in line_list if item != '']
			component_name = line_list[0]
			labels = '\n'.join(line_list[1:])
			dictionary[component_name] = labels

	# Based on these components, retrieve the top terms associated 
	# with a component. 
	top_terms_list = [] 
	components_label_list = []
	for top_component in top_components:
		with open(os.path.join(load_dir, top_component[3])) as f:
			file_lines = f.readlines()
			top_terms = dictionary[top_component[3]]
			top_terms_list.append(top_terms)

	top_loadings = [component[1] for component in top_components]

	# Put the data into appropriate format for radar plot.
	data = {
		'column names': top_terms_list,
		term: [top_loadings]
	}

	# Create the radar plot.
	radar_plot.one_panel_top_terms(data, outpath)


if __name__ == '__main__':

	# Radar plot
	ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'
	load_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/filtered_loadings'
	outpath = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/'\
				'visualization/moral/filtered/moral_top_15.png'
	dictionary_file = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
					'distribution/top_terms/task_terms_top.csv'
	radar_plot_top_terms("moral", ICA_path, load_dir, dictionary_file, outpath)

	# Radar plot.
	# radar_plot_top_terms("morality", ICA_path)

	# # Do descending loadings
	# # Load the graph.
	# graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
	# 'pickles/reverse_graph2.p'
	# graph = ns.LoadGraph(graph_pth)
	# terms = graph.vs['term']
	# ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/SHUFFLED2/'
	# main_out = os.path.join(ICA_path, 'loadings')
	# descendingLoadings(ICA_path, main_out)
