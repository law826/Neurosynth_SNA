"""
Rank terms according to the number of outliers.
"""
import os, sys, csv
import numpy as np
from scipy.stats.mstats import zscore

csv_input = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/term_weights.csv'
csv_output = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/outlier_count.csv'


# Import CSV file.
with open(csv_input, 'rU') as f:
    reader = csv.reader(f)
    row_list = [row for row in reader]
    term_list = [list(row) for row in zip(*row_list)]

# Calculate the z-scores for each term.
z_tuples = []
for term in term_list:
	term_name = term[0]
	weight_list = [float(weight) for weight in term[1:]]
	weight_list = np.array(weight_list)

	z_score = zscore(weight_list)

	# Count the number of terms that are less than or greater than 3.
	greater_than = np.where(z_score > 3)[0].shape[0]
	less_than = np.where(z_score < -3)[0].shape[0]

	extremes = greater_than + less_than
	z_tuples.append((term_name, extremes))

# Rank the terms in a list according to this number. 
sorted_terms = sorted(z_tuples, 
			key=lambda component: component[1], reverse = True)

# Output to a CSV.
with open(csv_output, 'wb') as output:
    writer = csv.writer(output, dialect= 'excel')
    writer.writerows(sorted_terms)