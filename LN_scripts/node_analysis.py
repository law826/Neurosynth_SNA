# Set up.

# from __future__ import division
# import unittest
# from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
# try:
# 	from igraph import *
# except ImportError:
# 	raise ImportError, "The igraph module is required to run this program."
#import igraph

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns
#import database as db
#import ListClass as lc
import nibabel

def get_brain_means_and_standard_deviation():
	image_directory = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/' \
			'graph_analysis_data/NeurosynthMerge/Reverse_Inference2/'

	mask_brain = '/Users/ln30/Git/Neurosynth_SNA/LN_scripts/'\
			'MNI152_T1_2mm_brain.nii.gz'

	# Get paths for every image file in the directory.
	image_names = ns.GetFileNamesInDirectory(image_directory)


	mean_array = []
	std_array = []
	for image in image_names:
		image_nib = nibabel.load(os.path.join(image_directory,image))
		image_nump = image_nib.get_data()
		mask_nib = nibabel.load(mask_brain)
		mask_nump = mask_nib.get_data() <= 0

		# Mask the array.
		masked_image_nump = np.ma.array(image_nump, mask=mask_nump)

		# Find the mean within the whole brain mask and add to array.
		mean_array.append(masked_image_nump.mean())
		std_array.append(masked_image_nump.std())
	return mean_array, std_array

get_brain_means_and_standard_deviation()