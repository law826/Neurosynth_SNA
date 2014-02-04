#!/bin/python

"""
This will import an edgelist and perform many computations
based on the booleans indicated below.
"""

# Set up.
#from __future__ import division
#import unittes
#from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import database as db
import ListClass as lc

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/')
import node_analysis as na

##### Sequences of events.
create_edgelist_from_columns = False ##
create_cross_corr_table_from_columns = False
import_graph_from_edgelist = False ## Will otherwise load a pickle.
make_graph_undirected = False ##
strip_loops_from_graph = False ##
add_term_names = False 
add_number_of_studies = False
add_brain_means = False
print_node_attributes_to_csv = False
import_partials_from_table = False
assign_semantic_Jaccards = False
save_the_graph = False ##
######

edgelist = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'NeurosynthMerge/merged_edgelist/merged_edgelist.csv'

corr_table = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/validation/'\
			'merged_output/merged_correlation.csv'

pcorr_table = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/'\
			'graph_analysis_data/NeurosynthMerge/merged_correlation/'\
			'merged_pcorrelation.csv'

term_correlation_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/'\
					'validation/output/'

outdir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/'\
				'validation/merged_output/'

outpath = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'pickles/reverse_graph2.p'

master_csv_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/'\
			'graph_analysis_data/node_master.csv'

git_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/neurosynthgit/'



# Import all the relevant paths.
if create_edgelist_from_columns:
	file_names = ns.GetFileNamesInDirectory(term_correlation_dir)
	ns.CreateEdgelist(term_correlation_dir, file_names, outdir,
		'merged_edgelist')

if create_cross_corr_table_from_columns:
	file_names = ns.GetFileNamesInDirectory(term_correlation_dir)
	ns.CreateCrossCorrelationTable(term_correlation_dir, 
		file_names, corr_table)
	os.system('open %s' %corr_table)

if import_graph_from_edgelist:
	graph = ns.ImportNcol(edgelist)
else:
	graph = ns.LoadGraph(outpath)

if make_graph_undirected:
	graph.to_undirected(mode="collapse", combine_edges= "max")

if strip_loops_from_graph:
	graph = db.StripLoops(graph)

if add_term_names:
	neurosynth_dir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/neurosynthgit/' \
			'results/run2/Reverse_Inference/'

	raw_terms = ns.GetFileNamesInDirectory(neurosynth_dir)
	graph = ns.StripName(graph, raw_terms)

if add_number_of_studies:
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

if add_brain_means:
	means, std = na.get_brain_means_and_standard_deviation()
	graph.vs['brain_means'] = means
	graph.vs['brain_std'] = std

if print_node_attributes_to_csv:
	with open(master_csv_path, 'w') as text_file:
		text_file.write('term,numberofstudies,brain_means,brain_std\n')
		for i, node in enumerate(graph.vs):
			text_file.write('%s,%s,%s,%s\n' %(
				graph.vs['term'][i],
				graph.vs['numberofstudies'][i],
				graph.vs['brain_means'][i],
				graph.vs['brain_std'][i]
				))
	os.system('open %s' %master_csv_path)

if import_partials_from_table:
	ns.Import_Edges_from_Table(graph, pcorr_table, 'partialcorrelation')

if assign_semantic_Jaccards:
	# Get term from thesaurus.
	aa = ns.ArticleAnalysis(git_path)
	jaccards = aa.CalculateMergedJaccards(graph)
	graph.es['jaccards'] = jaccards

if save_the_graph:
	ns.SaveGraph(graph, outpath)

try:
	os.system(
		"""osascript -e 'tell app "System Events" to display""" \
		""" dialog "Your script has finished running."'""")
except:
	pass