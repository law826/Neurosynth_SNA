"""
Making a heatmap from the table of cross correlations from the 
thesaurus merged data.
Created 11/27/13.
"""

cross_correlation_table = '/Volumes/huettel/KBE.01/Analysis/' \
	'Neurosynth/graph_analysis_data/NeurosynthMerge/merged_correlation/' \
	'merged_correlation.csv'

outdir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data' \
		'/graph_stats/visualizations/correlation_table_heatmap'

import numpy
from matplotlib import pyplot as plt
import re

#Convert from excel \r format to \n.
# with open(cross_correlation_table, 'r+') as excel_csv:
# 	raw = excel_csv.read()
# 	replaced = re.sub('\r', '\n', raw)

# with open(processed_correlation_table, 'wb') as output:
# 	output.write(replaced)


np_table = numpy.genfromtxt(
	open(cross_correlation_table,'rb'), delimiter=',')

# Extract only data and normalize.
data_only = np_table[1:, 1:]

data_norm = ((data_only - data_only.mean())/(data_only.max() - data_only.min()))

# Draw the heatmap.
heatmap = plt.pcolor(data_norm, cmap=plt.cm.Blues)
axes_limits = [0, 414, 0, 414]
plt.axis(axes_limits)
plt.xlabel('Term Number')
plt.ylabel('Term Number')


plt.savefig(outdir)



## Bugs.
# # If get ValueError: Some errors were detected !
#     Line #2 (got 414 columns instead of 684342)
#     Line #3 (got 414 columns instead of 684342)
#     Line #4 (got 414 columns instead of 684342)
#     Line #5 (got 414 columns instead of 684342)

# Then you may have run the script too many times and the csv appends to the 
# end. Try regenerating csv from Rstudio and rerunning first time through.
