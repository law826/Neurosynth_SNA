"""
Rank terms according the difference between the two most extreme positive values.
"""
import os, sys, csv
import numpy as np
from scipy.stats.mstats import zscore

csv_input = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'\
			'distribution/term_weights.csv'
csv_output = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'\
			'distribution/outlier_difference_count.csv'


# Import CSV file.
with open(csv_input, 'rU') as f:
    reader = csv.reader(f)
    row_list = [row for row in reader]
    term_list = [list(row) for row in zip(*row_list)]

diff_pairs = []
for term in term_list:
	term_name = term[0]
	weight_list = [float(weight) for weight in term[1:]]
	weight_list = np.array(weight_list)

	# Order weight list.
	sorted_weight_list = np.sort(weight_list)
	difference_of_top_two = sorted_weight_list[-1] - sorted_weight_list[-2]
	diff_pairs.append([term_name, difference_of_top_two])

# Rank the terms in a list according to this number. 
sorted_terms = sorted(diff_pairs, 
			key=lambda component: component[1], reverse = True)

# Output to a CSV.
with open(csv_output, 'wb') as output:
    writer = csv.writer(output, dialect= 'excel')
    writer.writerows(sorted_terms)