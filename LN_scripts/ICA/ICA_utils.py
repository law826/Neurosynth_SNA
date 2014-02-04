import os, glob

def descendingLoadings(ICA_path, terms, main_out):
	"""
	Given an ICA directory, output terms and loadings in descending order 
	for each each component into CSVs.

	- Implemented in get_shuffle_terms
	"""

	# Make main output directory if it does not exist. 
	if not os.path.exists(main_out):
		os.makedirs(main_out)

	# Get components.
	report_dir = os.path.join(ICA_path, 'report')
	component_files = glob.glob1(report_dir, "t*.txt")

	# Loop through components.
	for c_number, component_file in enumerate(component_files):
		# Load in lines as list.
		with open(os.path.join(report_dir, component_file), 'rb') as f:
			timepoints = [float(line.rstrip()) for line in f]
		component_tuples = [(terms[i], timepoints[i]) 
							for i, term in enumerate(terms)]
		sorted_cts = sorted(component_tuples, 
						key=lambda component: component[1], reverse = True)

		# Write to file.
		with open(os.path.join(
			main_out, 'component_%s.txt' %(c_number+1)), 'wb') as o:
			for i, sorted_ct in enumerate(sorted_cts):
				o.write('%s,%s\n' %(sorted_ct[0], sorted_ct[1]))

def get_sorted_list_by_term(term, load_dir, sort_list=True):
	"""
	Get a sorted list given a term and ICA_path. Several other pieces of 
	information are included as well.
	"""
	# Search a directory for all lines that include a certain term.
	component_files = glob.glob1(load_dir, "*.txt")

	# Collect all of these into tuples, which includes the component name.
	inter_line_list = [] 
	for component_file in component_files:
		with open(os.path.join(load_dir, component_file), 'rb') as f:
			file_lines = f.readlines()
			for file_line in file_lines:
				if term in file_line: 
					file_line = file_line.replace('\n', '')
					intra_line_list = file_line.split(',')
					# Make sure no nested terms.
					if intra_line_list[0] == term:
						intra_line_list[1] = float(intra_line_list[1])
						numeral_component = component_file.replace('component_', '')
						numeral_component = numeral_component.replace('.txt', '')
						intra_line_list.append(int(numeral_component))
						intra_line_list.append(component_file)
						inter_line_list.append(intra_line_list)

	# Sort by loadings.
	sorted_inter_line_list = sorted(inter_line_list, key = lambda ill: ill[1],
							reverse = True)

	if sort_list:
		return sorted_inter_line_list
	else:
		return inter_line_list