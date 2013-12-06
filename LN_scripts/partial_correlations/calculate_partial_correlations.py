"""
Takes a cross correlation matrix and outputs a partial correlation matrix.
"""

import numpy as np

cc_matrix_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/'\
			'graph_analysis_data/NeurosynthMerge/merged_correlation/'\
			'merged_correlation.csv'

# Load the cross correlation matrix.
cc_matrix = np.loadtxt(open(cc_matrix_path,'rb'),delimiter=',')
cc_matrix = cc_matrix[1:,1:]


p_inverted_cc = np.linalg.pinv(cc_matrix)

#det_cc = np.linalg.det(cc_matrix)
#inverted_cc = np.linalg.inv(cc_matrix)


import pdb; pdb.set_trace()

# Isolate the relevant part of the matrix.


# Calculate the 