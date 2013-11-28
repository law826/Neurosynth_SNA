#!/bin/python

"""
Using the thesaurus-merged data to create a cross correlation table.
Created 11/27/13.
"""

from __future__ import division
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np

sys.path.append('/Users/ln30/Git/Neurosynth_SNA/')
import Neurosynth_SNA as ns

# Import all the relevant paths.
term_correlation_dir = os.path.join('/Volumes', 'huettel', 'KBE.01', 
                'Analysis', 'Neurosynth', 'correlations_raw_data', 'run2', 
                'Reverse_Inference2')

outdir = '/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data/' \
			'NeurosynthMerge/merged_correlation/'

# Generate the file names of the input directory
file_names = ns.GetFileNamesInDirectory(term_correlation_dir)

# Generate a cross correlation table.
ns.CreateCrossCorrelationTable(term_correlation_dir, file_names, outdir,
	'merged_correlation')

"""
def GetFileNamesInDirectory(directory):
    Takes a directory and returns a list of the names of all the files in that 
    directory sorted in alphabetical order. 


ns.CreateCrossCorrelationTable(term_correlation_dir, )


def CreateCrossCorrelationTable(maindir, file_names, outdir, outname):

    Takes a directory and list of numpy files and horizontally concatenates 
    them all and saves the output in outdir. Labels are also added.
"""