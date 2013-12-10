"""
Making a heatmap from the table of cross correlations from the 
thesaurus merged data.
Created 11/27/13.
"""

cross_correlation_table = '/Volumes/huettel/KBE.01/Analysis/' \
	'Neurosynth/graph_analysis_data/NeurosynthMerge/merged_correlation/' \
	'merged_pcorrelation.csv'


outdir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data' \
		'/graph_stats/visualizations/correlation_table_heatmap'

import numpy
from matplotlib import pyplot as plt

np_table = numpy.loadtxt(
	open(cross_correlation_table,'rb'), delimiter=',')

# Extract only data and normalize.
data_only = np_table[1:,1:]

data_norm = ((data_only - data_only.mean())/ \
			(data_only.max() - data_only.min()))

# Draw the heatmap.
heatmap = plt.pcolor(data_norm, cmap=plt.cm.Blues)
axes_limits = [0, 414, 0, 414]
plt.axis(axes_limits)
plt.xlabel('Term Number')
plt.ylabel('Term Number')


plt.savefig(outdir)


import pdb; pdb.set_trace()