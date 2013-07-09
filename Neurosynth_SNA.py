#!/usr/bin/env python
# encoding: utf-8
"""
Neurosynth_SNA.py

[] test whether current import protocol works
[] add functionality for windows

"""
from __future__ import division
import os, sys, getpass
import random as rand
import cPickle
import numpy as np
from igraph import *
from pdb import *


def SetPaths():
	"""
	Set relevant paths for windows, linux, and mac systems.
	"""
	if sys.platform == "darwin":
		maindir = os.sep.join(['/Volumes', 'huettel', 'KBE.01',  'Analysis', 'Neurosynth', 'ReverseResults'])
		outdir  = os.sep.join(['/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
	elif sys.platform == "win32":
		maindir = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'ReverseResults'])
		outdir  = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
	elif sys.platform == "linux2":
		username=getpass.getuser()
		maindir = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'ReverseResults'])
		outdir  = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])

	forward_inference_edgelist = os.sep.join([outdir, "forward_inference.txt"])
	reverse_inference_edgelist = os.sep.join([outdir, "reverse_inference.txt"])

	return maindir, outdir, forward_inference_edgelist, reverse_inference_edgelist


def GetFileNamesInDirectory(directory):
	"""
	Takes a directory and returns a list of the names of all the files in that directory sorted in alphabetical order. 
	"""
	for files in os.walk(directory):
		for file in files:
			file_names=file
	file_names.sort()

	return file_names

def create_cross_correlation_table(maindir, files_names, outdir, outname):
	"""
	Takes a directory and list of numpy files and horizontally concatenates them all and saves the output in outdir. 
	"""
	for brain in range(0,979):
		database_brain = np.load(maindir+os.sep+file_names[brain]) # Loading the image
		#database_brain_data = database_brain.get_data() # Accessing numbers from the nibabel object and putting in numpy array.
		if brain==0:
			concatenate_data= database_brain
		else:
			concatenate_data=np.concatenate((concatenate_data, database_brain), axis=1)
	outpath=os.sep.join([outdir, outname])
	np.save(outpath, concatenate_data)
		
def CreateEdgelist(maindir, file_names, outdir, outname):
	"""
	Takes a directory and list of numpy files and vertically concatenates them into an edge list format and saves the output in outdir.
	"""
	for i, file_name in enumerate(file_names):
		database_brain      = np.load(maindir+os.sep+file_name) # Loading the data
		first_column        = np.zeros((database_brain.shape[0],1))
		first_column[:,0]   = i
		second_column       = np.arange((database_brain.shape[0]))
		second_column.shape = (database_brain.shape[0],1)
		three_col           = np.concatenate((first_column, second_column, database_brain), axis=1)
		if i==0:
			concatenate_data = three_col
		else:
			concatenate_data = np.concatenate((concatenate_data, three_col), axis=0)
	outpath=os.sep.join([outdir, outname])
	np.save(outpath, concatenate_data)
	set_trace()
	np.savetxt(outpath+'.txt', concatenate_data, fmt='%10.f %10.f %1.3f', delimiter='\t')

def ImportEdgelist(file):
	graph = Graph.Read_Edgelist(file)
	return graph

def VisualizeData():
	pass

def CommonCommands():
	graph = ImportData(forward_inference_edgelist)


"""
Start of specific user commands.
"""

def main():
	pass
	
if __name__ == '__main__':
	maindir, outdir, forward_inference_edgelist, reverse_inference_edgelist = SetPaths()
	file_names                                                              = GetFileNamesInDirectory(maindir)

	CreateEdgelist(maindir, file_names, outdir, 'reverse_inference2')



