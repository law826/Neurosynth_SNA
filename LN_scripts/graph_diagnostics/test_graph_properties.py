#!/usr/loca/bin/python

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

	def test_Directedness(self):
		self.graph.is_directed() == False

	def test_NodeNames(self):
		"""
		Make sure the names of the nodes are correct.
		"""
		first_five = ['1back', '2back', 'ability', 'acoustic', 'acquisition']
		last_five = ['word', 'work', 'working', 'writing', 'written']
		self.assertEqual(self.graph.vs['term'][0:5], first_five)
		self.assertEqual(self.graph.vs['term'][-5:], last_five)

	def test_NumberOfStudies(self):
		"""
		Tests whether the number of studies are correct. This should be post
		merge.
		"""
		first_five = [37, 84, 220, 106, 304]
		last_five = [1202, 846, 472, 33, 71]
		self.assertEqual(first_five, self.graph.vs['numberofstudies'][0:5])
		self.assertEqual(last_five, self.graph.vs['numberofstudies'][-5:])

	def test_ArticleJaccard(self):
		jaccards = self.graph.es['jaccards']
		self.assertEqual(len(jaccards), 85491)

		# All 1back and 2back are 'NA'. This should equal 413+412
		self.assertEqual(jaccards.count('NA', 825))

		# No Jaccards should be greater than 1.
		self.assertEqual(max(jaccard)<1, True)

		


	def test_is_done(self):
		try:
			os.system(
				"""osascript -e 'tell app "System Events" to display""" \
				""" dialog "Your script has finished running."'""")
		except:
			pass

	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after 
		each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()