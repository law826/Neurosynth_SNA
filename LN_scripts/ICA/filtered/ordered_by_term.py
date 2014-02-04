"""
Take from a filtered list of components and give a ordered list of each term.
Also will do the derivative max cutoff algorithm.
"""

import os, sys, operator, numpy as np
from scipy import cluster


sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
from ICA_utils import get_sorted_list_by_term


# This is only a subset of all the components, which eliminates both 
# artifactual components and subject-related components.
components_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
				'filtered_loadings/'

pre_sorted_list = get_sorted_list_by_term('moral', components_dir)

pre_sorted_list = [item[:3] for item in pre_sorted_list]

# Difference of contiguous sorted terms.
difference_array = [pre_sorted_list[i][1]-item[1]
					for i,item in enumerate(pre_sorted_list[1:])]

# Add the difference array to the matrix.
matrix = [item + [difference_array[i-1]]
			if i != 0
			else item
			for i, item in enumerate(pre_sorted_list)
			]

weights = [item[1] for item in pre_sorted_list]
weights = np.array(weights)

max_index, max_value = max(enumerate(difference_array, key=operator.itemgetter(1))

np_diff = np.array(difference_array)


centers, dist = cluster.vq.kmeans(weights, 2)
code, dist = cluster.vq.vq(weights, centers)



import pdb; pdb.set_trace()


