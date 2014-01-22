"""
Calculates the kurtosis of the weight distributions for each term.
"""

# Set up.
from __future__ import division
import unittest
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import igraph
import glob
import csv
from scipy.stats import kurtosis

input_csv = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'\
				'distribution/term_weights.csv'
csv_out = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'\
				'distribution/kurtosis.csv'

# Open and transpose csv.
with open(input_csv, 'rU') as f:
	reader = csv.reader(f)
	row_list = [row for row in reader]
	column_list = [list(row) for row in zip(*row_list)]

output = []
for column in column_list:
	term_name = column[0]
	weights = [float(weight) for weight in column[1:]]
	np_weights = np.array(weights)
	k = kurtosis(np_weights)
	output.append([term_name, k])

# Sort based on kurtosis.
sorted_output = sorted(output, key=lambda pair: pair[1])
sorted_output.reverse()
sorted_output.insert(0, ['term', 'kurtosis'])

# Output to CSV.
with open(csv_out, 'wb') as o:
	writer = csv.writer(o)
	writer.writerows(sorted_output)
