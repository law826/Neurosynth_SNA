"""
Various tests for ICA. 
"""

from __future__ import division
import unittest
import os, sys
from igraph import *
sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import csv

class TestDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_raw_weights_and_weight_summaries(self):
        """
        Make sure that the numbers going into the histogram and the one going into
        the summary excel sheet are the same. 
        """
        term_weights = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
                        'distribution/term_weights.csv'
        weight_summary = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/'\
                        'ICA65/distribution/gini_data.csv'

        with open(term_weights, 'rb') as tw:
            reader = csv.reader(tw)
            row_list = [row for row in reader]
            column_list = [list(row) for row in zip(*row_list)]

        # Make sure everything is still the right shape.
        self.assertEqual(len(column_list), 414)
        self.assertEqual(len(row_list), 66) # One more than # components.

        # 



    def tearDown(self):
        """
        If this method is defined, the test runner will invoke this after 
        each test. 
        """
        pass

if __name__ == '__main__':
    unittest.main()