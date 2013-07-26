from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
try:
	from igraph import *
except ImportError:
	raise ImportError, "The igraph module is required to run this program."

sys.path.append(os.path.realpath('..'))
import Neurosynth_SNA as ns


class TestDatabase(unittest.TestCase):

	def setUp(self):
		self.maindir, self.outdir, self.importdir, self.forward_inference_edgelist, self.reverse_inference_edgelist, self.f_pickle_path, self.r_pickle_path = ns.SetPaths()

	def test_GetFileNamesInDirectory(self):
		files = ns.GetFileNamesInDirectory('/Volumes/huettel/KBE.01/Analysis/Neurosynth/ReverseResults/')

		self.assertEqual(len(files), 525)
		self.assertNotEqual(files[0], '_DS.Store')

	def test_graph_vertices_and_edges(self):
		number_of_vertices = 525
		number_of_edges = (275625-525)/2

		fg = ns.LoadGraph(self.f_pickle_path)
		rg = ns.LoadGraph(self.r_pickle_path)

		for graph in [fg, rg]:
			self.assertEqual(len(graph.vs), number_of_vertices)
			self.assertEqual(len(graph.es), number_of_edges)
			self.assertEqual(all(graph.is_loop()), False)

	def test_Beam_sub_reverse_graph_concept(self):
		srg_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/SNAFiles/sub_reverse_graph_concept.p'
		srg = cPickle.load(open(srg_path, 'r'))
		pass

	def test_NeurosynthMerge(self):
		"""
		Make sure the number of images matches that predicted by the thesaurus merging.
		"""
		from Neurosynth_SNA import NeurosynthMerge
		thesaurus = [('emotion', 'emotions', 'emotion*'), ('intention', 'intentions', 'intention*')]
		npath = '/Users/law826/Dropbox/neurosynthgit'
		outpath = None
		nsm = NeurosynthMerge(thesaurus, npath, outpath)
		self.assertEqual(len(nsm.feature_list), 523)
		self.assertEqual('emotion' in nsm.feature_list, False)
		self.assertEqual('emotions' in nsm.feature_list, False)
		self.assertEqual('intention' in nsm.feature_list, False)
		self.assertEqual('intentions' in nsm.feature_list, False)
		self.assertEqual('intention*' in nsm.feature_list, True)
		self.assertEqual('emotion*' in nsm.feature_list, True)

	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()