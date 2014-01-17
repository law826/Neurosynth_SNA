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

def open_csv_and_transpose_to_list_of_lists(CSV_path):
	pass