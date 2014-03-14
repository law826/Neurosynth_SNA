"""
Cluster the ICA components hierarchically using terms as observations.
"""

import os, sys, glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram

load_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/filtered_loadings/'
component_files = glob.glob1(load_dir, "*.txt")
savepath = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/distribution/hierarchical.png'

# Terms to exclude 

# toe = ['adhd', 'adolescence', 'adults', 'age', 'agerelated', 'aging', 
# 		'allele', 'autism', 'bipolar', 'child', 'development', 'elderly', 
# 		'epilepsy', 'family', 'female', 'genotype', 'illness', 'male', 
# 		'polymorphism', 'ptsd', 'schizophrenia', 'sex', 'sexual', 'women']

matrix = np.empty((50, 414))
for i, component_file in enumerate(component_files):
	with open(os.path.join(load_dir, component_file), 'rb') as f:
		file_lines = f.readlines()

		# Alphabetize.
		file_lines = sorted(file_lines, key = lambda line: line.split(',')[0])

		# Filter out above terms.
		# file_lines = [file_line for file_line in file_lines 
		# 				if file_line.split(',')[0] not in toe]

		weights = [float(file_line.split(',')[1].replace('\n', '')) for file_line in file_lines]
		np_weights = np.array(weights)

		# Take numbers and assign to numpy array.
		matrix[i,:] = np_weights

# Find distance matrix. 
distanceMatrix = pdist(matrix)
linkageMatrix = linkage(distanceMatrix)
flatLinkage = fcluster(linkageMatrix, 2)


# Do hierarchical clustering. 

# Make a dendrogram.

ax = plt.figure(figsize=(10, 6))
dendrogram_labels = [component.replace('component_', '').replace('.txt', '')
						for component in component_files]
dendrogram(linkageMatrix, labels = dendrogram_labels)
plt.savefig(savepath)


