"""
Takes the paths from a shuffled iteration and gives back a list of term names.
"""

import os, sys

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/LN_scripts/ICA/')
from ICA_utils import descendingLoadings

ICA_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/ICA/SHUFFLED4/'
load_dir = os.path.join(ICA_path, 'loadings')

def get_shuffled_terms(shuffle_log_path):
	f = open(shuffle_log_path, 'rb') 
	lines = f.readlines()
	to_delete1 = '/home/ln30/linux/experiments/KBE.01/Analysis/Neurosynth/'\
				'neurosynthgit/results/run2/Reverse_Inference/'
	to_delete2 = '_pFgA_z.nii.gz\n'
	tmp_lines = [item.replace(to_delete1, '') for item in lines]
	tmp_lines = [item.replace(to_delete2, '') for item in tmp_lines]
	f.close()
	return tmp_lines

if __name__ == '__main__':
	shuffle_log_path = '/Volumes/Huettel/KBE.01/Analysis/Neurosynth/'\
				'neurosynthgit/results/run2/merged_images_ri/shuffled_log2.txt'
	shuffled_terms = get_shuffled_terms(shuffle_log_path)
	print shuffled_terms
	descendingLoadings(ICA_path, shuffled_terms, load_dir)