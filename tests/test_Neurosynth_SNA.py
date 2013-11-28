from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
try:
	from igraph import *
except ImportError:
	raise ImportError, "The igraph module is required to run this program."

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns


class TestDatabase(unittest.TestCase):

	def setUp(self):
		# self.paths includes a variety of relevant paths 
		# from Neurosynth_SNA.py.
		self.paths = ns.Paths()

	def test_GetFileNamesInDirectory(self):
		files = ns.GetFileNamesInDirectory(
			'/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
			'graph_analysis_data/NeurosynthMerge/Reverse_Inference2')
		# Round 2 after merging should only have 414 instead of 525 studies.
		self.assertEqual(len(files), 414) 
		self.assertNotEqual(files[0], '_DS.Store')


		

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

	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after 
		each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()