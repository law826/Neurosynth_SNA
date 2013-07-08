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
	if sys.platform == "darwin":
	    maindir = os.sep.join(['/Volumes', 'KBE.01',  'Analysis', 'Neurosynth', 'ReverseResults'])
	    outdir = os.sep.join(['/Volumes', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
	elif sys.platform == "win32":
	    maindir = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'ReverseResults'])
	    outdir = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
	elif sys.platform == "linux2":
		import getpass
		username=getpass.getuser()
		maindir = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'ReverseResults'])
		outdir = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
	for files in os.walk(maindir):
		for file in files:
			file_names=file
	file_names.sort()




	forward_inference_edgelist = "/Volumes/huettel/KBE.01/Analysis/Neurosynth/Data/forward_inference.txt"

def create_cross_correlation_table():
	for brain in range(0,979):
		database_brain = N.load(maindir+os.sep+file_names[brain]) # Loading the image
		#database_brain_data = database_brain.get_data() # Accessing numbers from the nibabel object and putting in numpy array.
		if brain==0:
			concatenate_data= database_brain
		else:
			concatenate_data=N.concatenate((concatenate_data, database_brain), axis=1)
	outpath=os.sep.join([outdir, 'concatenate_data_matrix'])
	N.save(outpath, concatenate_data)
		
def create_SNA_table():
	for i, file_name in enumerate(file_names):
		database_brain = N.load(maindir+os.sep+file_name) # Loading the data
		first_column=N.zeros((database_brain.shape[0],1))
		first_column[:,0]=i
		second_column=N.arange((database_brain.shape[0]))
		second_column.shape = (database_brain.shape[0],1)
		three_col = N.concatenate((first_column, second_column, database_brain), axis=1)
		if i==0:
			concatenate_data=three_col
		else:
			concatenate_data=N.concatenate((concatenate_data, three_col), axis=0)
	outpath=os.sep.join([outdir, 'reverse_inference'])
	N.save(outpath, concatenate_data)
	N.savetxt(outpath+'.txt', concatenate_data, fmt='%10.f %10.f %1.3f', delimiter='\t')

def ImportData(file):
	graph = Graph.Read_Edgelist(file)
	return graph

def VisualizeData():
	pass

def CommonCommands():
	graph = ImportData(forward_inference_edgelist)

if __name__ == '__main__':
	SetPaths()

