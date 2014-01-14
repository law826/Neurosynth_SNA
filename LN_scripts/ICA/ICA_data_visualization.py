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

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
import radar_plot

def descendingLoadings(ICA_path, main_out):
	"""
	Given an ICA directory, output terms and loadings in descending order 
	for each each component into CSVs.
	"""

	# Make main output directory if it does not exist. 
	if not os.path.exists(main_out):
		os.makedirs(main_out)

	# Get components.
	report_dir = os.path.join(ICA_path, 'report')
	component_files = glob.glob1(report_dir, "t*.txt")

	# Loop through components.
	for c_number, component_file in enumerate(component_files):
		# Load in lines as list.
		with open(os.path.join(report_dir, component_file), 'rb') as f:
			timepoints = [float(line.rstrip()) for line in f]
		component_tuples = [(terms[i], timepoints[i]) 
							for i, term in enumerate(terms)]
		sorted_cts = sorted(component_tuples, 
						key=lambda component: component[1], reverse = True)

		# Write to file.
		with open(os.path.join(
			main_out, 'component_%s.txt' %(c_number+1)), 'wb') as o:
			for i, sorted_ct in enumerate(sorted_cts):
				o.write('%s,%s\n' %(sorted_ct[0], sorted_ct[1]))

def radar_plot_top_terms(term, ICA_path):
	"""
	Takes a term and makes a radar plot of the top associated terms.
	"""
	
	# Search a directory for all lines that include a certain term.
	load_dir = os.path.join(ICA_path, 'loadings')
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
					intra_line_list[1] = float(intra_line_list[1])
					numeral_component = component_file.replace('component_', '')
					numeral_component = numeral_component.replace('.txt', '')
					intra_line_list.append(int(numeral_component))
					intra_line_list.append(component_file)
					inter_line_list.append(intra_line_list)

	# Sort by loadings. 
	sorted_inter_line_list = sorted(inter_line_list, key = lambda ill: ill[1],
							reverse = True)

	# Retrieve the top 9.
	num_top_items = 9
	num_top_terms = 4
	top_components = sorted_inter_line_list[:num_top_items]

	# Based on these components, retrieve the top 4 terms associated 
	# with a component. 
	top_terms_list = [] 
	for top_component in top_components:
		with open(os.path.join(load_dir, top_component[3])) as f:
			file_lines = f.readlines()
			top_lines = file_lines[:num_top_terms]
			top_terms = [line.split(',')[0] for line in top_lines]
			top_terms = '\n'.join(top_terms)
			top_terms_list.append(top_terms)

	top_loadings = [component[1] for component in top_components]

	# Put the data into appropriate format for radar plot. 
	data = {
		'column names': top_terms_list,
		term: [top_loadings]
	}

	# Create the radar plot.
	radar_plot.one_panel_top_terms(data)


if __name__ == '__main__':



	# Radar plot
	ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/merged_rTPJ_free_ICA/'
	radar_plot_top_terms("rTPJ", ICA_path)

	# Radar plot.
	# radar_plot_top_terms("morality", ICA_path)

	# # Do descending loadings
	# # Load the graph.
	# graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
	# 'pickles/reverse_graph2.p'
	# graph = ns.LoadGraph(graph_pth)
	# terms = graph.vs['term']
	# terms.append('rTPJ')
	# ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/merged_rTPJ_free_ICA/'
	main_out = os.path.join(ICA_path, 'loadings')
	descendingLoadings(ICA_path, main_out)
