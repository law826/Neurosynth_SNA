"""
Makes a csv with terms arranged by component number.
"""

import os, sys, csv
import numpy as np
from scipy.stats.mstats import zscore

csv_input = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/term_weights.csv'
csv_output = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/term_by_component.csv'


# Import CSV file.
with open(csv_input, 'rU') as f:
    reader = csv.reader(f)
    row_list = [row for row in reader]
    term_list = [list(row) for row in zip(*row_list)]

output = []
for term in term_list:
	term_name = term[0]
	weight_list = [float(weight) for weight in term[1:]]
	labeled_wl = [(i+1, weight) for i,weight in enumerate(weight_list)]

	sorted_lwl = sorted(labeled_wl, 
			key=lambda component: component[1], reverse = True)

	sorted_components = [pair[0] for pair in sorted_lwl]
	sorted_components.insert(0, term_name)

	output.append(sorted_components)

trans_output = [list(row) for row in zip(*output)]

# Output to a CSV.
with open(csv_output, 'wb') as output:
    writer = csv.writer(output, dialect= 'excel')
    writer.writerows(trans_output)