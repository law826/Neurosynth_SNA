#!/bin/python
"""
Take in a CSV generate a text file that can serve as input into Wordle.
Right now, it only takes the second column and multiplies based on 
that count.
"""

import csv
import math


# Input file.
merged_master_path = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
	'graph_analysis_data/graph_stats/merged_graph_master.csv'

# Output file.
output_text_file = '/Users/ln30/Git/Neurosynth_SNA/' \
	'data_visualization/wordle_string.txt'



with open(merged_master_path, 'rU') as csvfile:
	# Open a CSV object that can be iterated. 
	csv_object = csv.reader(csvfile, delimiter=',',
		dialect=csv.excel_tab)
	# Dump CSV objects items into a python list.
	py_list = []
	for row in csv_object:
		py_list.append(row)

# Get rid of first row.
del py_list[0]

# Refine to a list of just the first and second columns.
# Make the second column a float.
# Add a constant so all numbers all positive.
# Round down the number so that it is an int.
# Amplify the difference for visualization.
wordle_list = [(x[0],20*math.trunc(float(x[1])+20)) for x in py_list]

# Make a massive concantenated string.
wordle_string=str()
for term in wordle_list:
	wordle_string += (term[0]+ ' ') * int(term[1])

with open(output_text_file, 'w') as text_file:
	text_file.write(wordle_string)





