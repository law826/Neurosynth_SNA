"""
Takes each components and outputs the top terms, defined as the terms above
the biggest jump in weights.
"""

import os, sys, glob, csv
import pylab as plt

ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65'
csv_output = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/top_terms/dictionary.csv'

difference_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
			'distribution/top_terms/differences/plots'

# Import files.
load_dir = os.path.join(ICA_path, 'filtered_loadings')
component_files = glob.glob1(load_dir, "*.txt")

# Collect all of these into tuples, which includes the component name.
out_list = []
diff_list = []
for i, component_file in enumerate(component_files):
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
			else:
				intra_line_list.append(0)
			intra_line_list.append(i+1)

			matrix.append(intra_line_list)

		# Add raw data so that differences can be printed. 
		diff_list.append(matrix)
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
# with open(csv_output, 'wb') as output:
#     writer = csv.writer(output, dialect= 'excel')
#     writer.writerows(out_list)

# Output diff list to csv.
# for i, component in enumerate(diff_list):
# 	diff_path = os.path.join(difference_dir, 'component_%s.csv' %(i+1)) 
# 	with open(diff_path, 'wb') as do:
# 		writer = csv.writer(do, dialect= 'excel')
# 		writer.writerows(component)

# Make scatterplots.
for i, component in enumerate(diff_list):
	transposed = [list(row) for row in zip(*component)]
	ax = plt.figure(figsize=(20,12))
	plt.xlabel('Nth Component Jump', fontsize=30)
	plt.ylabel('Difference in Weight', fontsize=30)
	plt.xlim([0, 414])
	# plt.ylim([0, 3])
	plt.tick_params(axis='x', labelsize=24)
	plt.tick_params(axis='y', labelsize=24)
	plt.tight_layout()
	plt.plot(transposed[3][1:], transposed[2][1:], '.b-', linewidth=3.0)
	plt.savefig(os.path.join(difference_dir, '%s.png' %out_list[i][0]))