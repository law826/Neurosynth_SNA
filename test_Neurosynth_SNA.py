from __future__ import division
import Neurosynth_SNA as ns
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
try:
	from igraph import *
except ImportError:
	raise ImportError, "The igraph module is required to run this program."


class TestDatabase(unittest.TestCase):

	def setUp(self):
		self.maindir, self.outdir, self.importdir, self.forward_inference_edgelist, self.reverse_inference_edgelist, self.f_pickle_path, self.r_pickle_path = ns.SetPaths()

	def test_GetFileNamesInDirectory(self):
		files = ns.GetFileNamesInDirectory('/Volumes/huettel/KBE.01/Analysis/Neurosynth/ReverseResults/')

		self.assertEqual(len(files), 525)
		self.assertNotEqual(files[0], '_DS.Store')

	def test_Graph(self):
		fg = ns.LoadGraph(self.f_pickle_path)
		rg = ns.LoadGraph(self.r_pickle_path)

		for graph in [fg, rg]:
			self.assertEqual(len(graph.vs), 525)
			self.assertEqual(len(graph.es), ((275625-525)/2))
			[edge.is_loop() for edge in fg.es if edge.is_loop == True]
			#137550

	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()