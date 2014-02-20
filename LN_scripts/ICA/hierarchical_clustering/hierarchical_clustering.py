"""
Cluster the ICA components hierarchically using terms as observations.
"""

import os, sys, glob
import numpy as np
import matplotlib.pyplot as plt

load_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/filtered_loadings/'
component_files = glob.glob1(load_dir, "*.txt")

matrix = np.empty((65, 414))
for i, component_file in enumerate(component_files):
	with open(os.path.join(load_dir, component_file), 'rb') as f:
		file_lines = f.readlines()

		file_lines = sorted(file_lines, key = lambda line: line.split(',')[0])


		weights = [float(file_line.split(',')[1].replace('\n', '')) for file_line in file_lines]
		np_weights = np.array(weights)

		matrix[i,:] = np_weights
		matrix = np.concatenate((matrix, np_weights), axis=0)

import pdb; pdb.set_trace()

# Read in /Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/loadings/component_1.txt
# files.
 
# Alphabetize. 

# Take numbers and assign to numpy array.

# Find distance matrix. 


# Do hierarchical clustering. 

# Make a dendrogram.


