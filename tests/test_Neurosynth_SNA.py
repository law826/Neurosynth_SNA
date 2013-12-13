from __future__ import division
import unittest
import os, sys
from igraph import *
sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns

class TestDatabase(unittest.TestCase):

	def setUp(self):
		self.graph = Graph.Full(3)
		self.graph.es['weight'] = 1.0
		self.graph.es['weight'] = [0.9, 0.1, 0.6] # Tuples are (0,1), (0,2), (1,2)

	def test_centralities(self):
		degree_centrality = self.graph.strength(loops=False, weights='weight')
		betweenness_cent = self.graph.betweenness(directed=False, 
					weights='weight')
		eigenvector_cent = self.graph.evcent(directed=False, weights='weight')
		closeness_cent = self.graph.closeness(weights='weight')

		self.assertEqual(degree_centrality, [1.0, 1.5, 0.7])
		self.assertEqual(betweenness_cent, [0, 0, 1])

		eigenvector_rounded = [round(x, 2) for x in eigenvector_cent]
		self.assertEqual(eigenvector_rounded, [0.85, 1.0, 0.61])

		closeness_rounded = [round(x, 2) for x in closeness_cent]
		self.assertEqual(closeness_rounded, [2.5, 1.54, 2.86])

		import pdb; pdb.set_trace()


	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after 
		each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()


#####
	# def test_GetFileNamesInDirectory(self):
	# 	files = ns.GetFileNamesInDirectory(
	# 		'/Volumes/huettel/KBE.01/Analysis/Neurosynth/'
	# 		'graph_analysis_data/NeurosynthMerge/Reverse_Inference2')
	# 	# Round 2 after merging should only have 414 instead of 525 studies.
	# 	self.assertEqual(len(files), 414) 
	# 	self.assertNotEqual(files[0], '_DS.Store')	

	# def test_ArticleAnalysis(self):
	# 	npath = self.paths.git_path
	# 	# # term = 'emo*'
	# 	aa = ns.ArticleAnalysis(npath)

	# 	directory = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
	# 	'graph_analysis_data/graph_stats/num_articles/'
	# 	graph_pickle = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
	# 	'graph_analysis_data/pickles/sub_reverse_graph_concept_with_Jaccards.p' 
	# 	aa.OutputJaccardsAndWeightsToFiles(graph_pickle, directory)		

		# number_of_terms = aa.CalculateNumberofArticles(term)
#    def OutputJaccardsAndWeightsToFiles(self, graph_pickle, directory):
		# self.assertEqual(number_of_terms, 639)

		# emo_jaccard = aa.CalculateJaccard('imagery', 'images')
		# self.assertEqual(emo_jaccard, (72/(92+1979+72)))

		# There are no tests for the following!
		# Beam_sub_graph = ns.LoadGraph('/Volumes/huettel/KBE.01/Analysis/
			# Neurosynth/' \
		#	'graph_analysis_data/pickles/sub_reverse_graph_concept.p')
		# aa.AssignJaccardsToGraph(Beam_sub_graph)

	# def test_graph_vertices_and_edges(self):
	# 	number_of_vertices = 525
	# 	number_of_edges = (275625-525)/2

	# 	fg = ns.LoadGraph(self.paths.f_pickle_path)
	# 	rg = ns.LoadGraph(self.paths.r_pickle_path)

	# 	for graph in [fg, rg]:
	# 		self.assertEqual(len(graph.vs), number_of_vertices)
	# 		self.assertEqual(len(graph.es), number_of_edges)
	# 		self.assertEqual(all(graph.is_loop()), False)

	# def test_Beam_sub_reverse_graph_concept(self):
	# 	srg_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/ \
		# graph_analysis_data/pickles/sub_reverse_graph_concept.p'
	# 	srg = cPickle.load(open(srg_path, 'r'))
	# 	pass

	# def test_NeurosynthMerge(self):
	# 	"""
	# 	Make sure the number of images matches that predicted by the 
	# thesaurus merging.
	# 	"""
	# 	from Neurosynth_SNA import NeurosynthMerge

	# 	# Inputs
	# 	thesaurus = [('emotion', 'emotions', 'emotion|emotions'), 
	# 				('intention', 'intentions', 'intention|intentions'),
	# 				('association', 'associations', 'associative', 
	#				'association|associations|associative')]
	# 	npath = '/Users/ln30/Dropbox/neurosynthgit/' # The only difference 
	#	between two computers is the username. 

	# 	outdir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/test'
	# 	if not os.path.exists(outdir):
	# 		os.makedirs(outdir)

	# 	# Instantiation
	# 	nsm = NeurosynthMerge(thesaurus, npath, outdir, test_mode=True)

	# 	# Tests
	# 	self.assertEqual(len(nsm.feature_list), 3)
	# 	self.assertEqual('emotion' in nsm.feature_list, False)
	# 	self.assertEqual('emotions' in nsm.feature_list, False)
	# 	self.assertEqual('intention' in nsm.feature_list, False)
	# 	self.assertEqual('intentions' in nsm.feature_list, False)
	# 	self.assertEqual('association' in nsm.feature_list, False)
	# 	self.assertEqual('associations' in nsm.feature_list, False)
	# 	self.assertEqual('associative' in nsm.feature_list, False)
	# 	self.assertEqual('intention|intentions' in nsm.feature_list, True)
	# 	self.assertEqual('emotion|emotions' in nsm.feature_list, True)
	# 	self.assertEqual(
	#	'association|associations|associative' in nsm.feature_list, True)