"""
Take from a filtered list of components and give a ordered list of each term.
Also will do the derivative max cutoff algorithm.
"""

import os, sys

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
from ICA_utils import get_sorted_list_by_term



# This is only a subset of all the components, which eliminates both 
# artifactual components and subject-related components.
components_dir = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/ICA65/'\
				'filtered_loadings/'

sorted_list = get_sorted_list_by_term('moral', components_dir)

import pdb; pdb.set_trace()


