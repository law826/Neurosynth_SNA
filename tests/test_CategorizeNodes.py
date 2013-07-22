from __future__ import division
import os, sys
import random as rand
import cPickle 
import numpy as np
import getpass
import nltk
from pdb import *
from igraph import *
import pickle
from Tkinter import *
import unittest

sys.path.append(os.path.realpath('..'))
import basefunctions
from CategorizeNodes import CategorizeNodesGUI
from CategorizeNodes import CNBridge

class TestCategorizeNodes(unittest.TestCase):
	def setUp(self):
		self.g = Graph()
		self.g.add_vertices(5)
		self.g.add_edges([(0,1), (0,2), (1,2)])
		self.g.vs["term"] = ['a','b','c','d', 'e']
		
	def test_correct_assignment_and_bridge_into_graph(self):
		"""
		Make sure that nodes a-e correspond to 3 brains and 2 concepts (in that order).
		"""
		self.cn = CategorizeNodesGUI(self.g.vs["term"], "test_CN.p")
		self.cn.SaveTupleFile()
		self.cn.LoadTupleFile()
		self.assertEqual(self.cn.tuple_list, [('a', 'brain'), ('b', 'brain'), ('c', 'brain'), ('d', 'concept'), ('e', 'concept')])
		cnb = CNBridge(self.g, "test_CN.p")
		cnb.LoadPickle()
		self.assertEqual([node['type'] for node in self.g.vs], ['brain', 'brain', 'brain', 'concept', 'concept'])

	def tearDown(self):
		"""
		If this method is defined, the test runner will invoke this after each test. 
		"""
		pass

if __name__ == '__main__':
	unittest.main()