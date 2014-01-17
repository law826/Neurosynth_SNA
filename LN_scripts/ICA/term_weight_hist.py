"""
Takes csv of term weights and makes a histogram for each term.
"""

import os, csv 
import pylab as P


csv_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
            'distribution/term_weights.csv'
outdir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
            'distribution/weight_histograms/'

with open(csv_path, 'rU') as f:
    reader = csv.reader(f)
    row_list = [row for row in reader]
    term_list = [list(row) for row in zip(*row_list)]

    for term in term_list:
        # Convert to float.
        term_name = term[0]
        weights = [float(item) for i,item in enumerate(term) if i != 0]
        histogram = P.hist(weights)
        P.xlabel('ICA temporal weight')
        P.ylabel('Number of Component')
        P.figtext(0.5, 0.965, term_name, ha='center', color='black', 
                    weight='bold', size='large')
        P.savefig(os.path.join(outdir, term_name))
        P.close()

sys.path.append('/Users/ln30/Git/general_scripts/')
import send_message; send_message.send_text()