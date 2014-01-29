"""
Filter kurtosis based on Ellie's subgraph.
"""
import os, sys, csv

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
from ListClass import ListClass

lc = ListClass()
sub_concepts = lc.sub_Beam_concepts
input_csv = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'\
				'distribution/outlier_difference_count.csv'
csv_out = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA20/'\
				'distribution/Beam_sub_outlier_difference.csv'

# Import CSV.
with open(input_csv, 'rU') as f:
	reader = csv.reader(f)
	row_list = [row for row in reader]

# Filter based on sub_concepts.
filtered = [row for row in row_list if row[0] in sub_concepts]

# Output to CSV.
with open(csv_out, 'wb') as o:
	writer = csv.writer(o)
	writer.writerows(filtered)
