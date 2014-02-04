"""
Takes each components and outputs the top terms, defined as the terms above
the biggest jump in weights.
"""

import os, sys, glob, csv

ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'
csv_output = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/top_terms/terms_only.csv'

# Import files.
load_dir = os.path.join(ICA_path, 'loadings')
component_files = glob.glob1(load_dir, "*.txt")

# Collect all of these into tuples, which includes the component name.
out_list = []
for component_file in component_files:
	with open(os.path.join(load_dir, component_file), 'rb') as f:
		file_lines = f.readlines()
		matrix = []
		for i, file_line in enumerate(file_lines):
			file_line = file_line.replace('\n', '')
			intra_line_list = file_line.split(',')
			intra_line_list[1] = float(intra_line_list[1])
			# If not the first row, add difference between weights as third
			# element.
			if i != 0:
				intra_line_list.append(matrix[i-1][1] - intra_line_list[1])
			matrix.append(intra_line_list)
		# Find the maximum weight in the matrix.
		diff_weights = zip(*matrix[1:])[2]
		max_value = max(diff_weights)
		max_index = diff_weights.index(max_value)
		# Because of blank 3rd element for first row...
		max_index = max_index + 1
		# Includes the first excluded term.
		components = matrix[:max_index] 
		# Convert back to strings.
		for item in components:
			try:
				item[1] = str(item[1])
				item[2] = str(item[2])
			except:
				pass
		components.insert(0, [component_file])
		# the following for comprehensive
		#components = ['_'.join(item) for item in components]
		components = [item[0] for item in components]
		out_list.append(components)

# Output to a CSV.
with open(csv_output, 'wb') as output:
    writer = csv.writer(output, dialect= 'excel')
    writer.writerows(out_list)


