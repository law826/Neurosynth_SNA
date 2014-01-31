"""
Puts terms into different categories.
"""

import os, sys, csv, igraph, collections

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
import ListClass 

listclass = ListClass.ListClass()
subject_terms = listclass.subject_related_terms

csv_input = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
            'distribution/top_terms/task_filtered.csv'

csv_output = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
            'distribution/top_terms/categorizations.csv'

graph_pth = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/'\
    'pickles/reverse_graph2.p'

graph = ns.LoadGraph(graph_pth)
terms = graph.vs['term']

# Import CSV file.
with open(csv_input, 'rU') as f:
    reader = csv.reader(f)
    row_list = [row for row in reader]

all_basic_terms = []
for row in row_list:
    basic_terms_row = [item for item in row[1:] if item != '']
    all_basic_terms += basic_terms_row

set_basic_terms = list(set(all_basic_terms))
duplicates = [x for x, y in collections.Counter(all_basic_terms).items() if y > 1]

pre_emergent_terms = [term for term in terms if term not in set_basic_terms]
emergent_terms = [term for term in pre_emergent_terms if term not in subject_terms]

set_basic_terms.insert(0, 'basic_terms')
emergent_terms.insert(0, 'emergent_terms')
subject_terms.insert(0, 'subject_terms')

matrix = []
matrix.append(set_basic_terms)
matrix.append(emergent_terms)
matrix.append(subject_terms)

# Output to a CSV.
with open(csv_output, 'wb') as output:
    writer = csv.writer(output, dialect= 'excel')
    writer.writerows(matrix)


import pdb; pdb.set_trace()
