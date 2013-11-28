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
		pickle_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
			'graph_analysis_data/pickles/reverse_graph2.p'

		# Load the graph.
		self.graph = ns.LoadGraph(pickle_path)

	def test_NumberOfNodes(self):
		# There should be 414 nodes in the graph.
		self.assertEqual(len(self.graph.vs), 414)

	def test_NumberOfEdges(self):
		# There should be 85491 edges.
		self.assertEqual(len(self.graph.es), 85491)
		# If it is 171,396, then this means that it includes directed edges.
		import pdb; pdb.set_trace()

	def test_NodeNames(self):
		"""
		Make sure the names of the nodes are correct.
		"""
		pass

	def test_NumberOfStudies(self):
		"""
		Tests whether the number of studies are correct.
		"""
		pass

	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after 
		each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()