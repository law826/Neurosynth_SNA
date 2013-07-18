#!/usr/bin/env python
# encoding: utf-8
"""
[] make functionality for starting from the beginning again.
[] test whether current import protocol works
[] add functionality for windows
"""
from __future__ import division
import database
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
try:
	from igraph import *
except ImportError:
	raise ImportError, "The igraph module is required to run this program."

def SetPaths():
	"""
	Set relevant paths for windows, linux, and mac systems.
	"""
	if sys.platform == "darwin":
		maindir = os.sep.join(['/Volumes', 'huettel', 'KBE.01',  'Analysis', 'Neurosynth', 'ForwardResults'])
		outdir  = os.sep.join(['/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles'])
		importdir  = os.sep.join(['/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
		r_pickle_path = os.sep.join(['/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles', 'reverse_graph.p'])
		f_pickle_path = os.sep.join(['/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles', 'forward_graph.p'])
	elif sys.platform == "win32":
		maindir = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'ForwardResults'])
		outdir  = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles'])
		importdir  = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
		r_pickle_path = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles', 'reverse_graph.p'])
		f_pickle_path = os.sep.join(['M:', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles', 'forward_graph.p'])
	elif sys.platform == "linux2":
		username=getpass.getuser()
		maindir = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'ForwardResults'])
		outdir  = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles'])
		importdir  = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'Data'])
		r_pickle_path = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles', 'reverse_graph.p'])
		f_pickle_path = os.sep.join(['/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'SNAFiles', 'forward_graph.p'])

	forward_inference_edgelist = os.sep.join([outdir, "forward_inference.txt"])
	reverse_inference_edgelist = os.sep.join([outdir, "reverse_inference.txt"])

	return maindir, outdir, importdir, forward_inference_edgelist, reverse_inference_edgelist, f_pickle_path, r_pickle_path

def GetFileNamesInDirectory(directory):
	"""
	Takes a directory and returns a list of the names of all the files in that directory sorted in alphabetical order. 
	"""
	for files in os.walk(directory):
		for file in files:
			file_names=file
	file_names.sort()

	try:
		file_names.remove('.DS_Store') # This is a file that mac systems automatically insert into directories and must be removed.
	except:
		pass

	return file_names

def CreateCrossCorrelationTable(maindir, file_names, outdir, outname):
	"""
	Takes a directory and list of numpy files and horizontally concatenates them all and saves the output in outdir. Labels are also added.
	"""
	for number, file_name in enumerate(file_names):
		database_brain = np.load(maindir+os.sep+file_name) # Loading the correlation column.
		if number==0:
			concatenate_data= database_brain
		else:
			concatenate_data=np.concatenate((concatenate_data, database_brain), axis=1)


	# Add concept indices:
	num_of_rows = concatenate_data.shape[0]
	horz_labels = np.arange(0, num_of_rows)
	horz_labels = np.expand_dims(horz_labels, axis=0) # Necessary for swapping and concatenating.
	vert_labels = np.swapaxes(horz_labels, 0, 1)
	horz_labels = np.insert(horz_labels, 0, 0)
	horz_labels = np.expand_dims(horz_labels, axis=0) # Expands again because the last line eliminates an axis for some reason.


	concatenate_data = np.concatenate((vert_labels, concatenate_data), axis=1)
	concatenate_data = np.concatenate((horz_labels, concatenate_data), axis=0)

	outpath=os.sep.join([outdir, outname])
	np.save(outpath, concatenate_data)
	np.savetxt(outpath+'.txt', concatenate_data, fmt='%10.3f', delimiter=',')
		
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
	np.savetxt(outpath+'.txt', concatenate_data, fmt='%1.f %1.f %1.3f')
	
def ImportAdjacencyMatrix(file):
	graph = Graph.Read_Adjacency(file)
	return graph

def ImportNcol(file):
	graph = Graph.Read_Ncol(file, names=True, weights=True)
	return graph

def VisualizeData():
	pass

def SaveGraph(graph, path):
	Graph.write_pickle(graph, path)
	
def CommonCommands():
	"""
	Random commands.
	"""
	graph = ImportData(forward_inference_edgelist)

def LoadGraph(pickle_path):
	graph = Graph.Read_Pickle(pickle_path)
	return graph

def StripName(graph, rawterms): 
	"""
	input: nameless graph, nonstripped list of terms(separated by underscores)
	output: graph of stripped terms (name of attribute= "term")
	"""
	graph.vs["term"]=rawterms # Set the names of the vertices.
	graph.vs["term"]=[x.split('_')[1] for x in graph.vs["term"]]
	return graph

####### Statistics
def VisualizeGraph(graph, outdir):
	graph.write_svg(outdir+os.sep+'forward_graph_kamada_kawai', labels = "name", layout = graph.layout_kamada_kawai())
	pass

def CalculateBetweennessCentrality(graph):
	pass




"""
Start of specific user commands.

To do list:
[] refine names to get rid of underscores and keep only first part (hint: string.sep('_'))
"""	
if __name__ == '__main__':
	maindir, outdir, importdir, forward_inference_edgelist, reverse_inference_edgelist, f_pickle_path, r_pickle_path = SetPaths()
	fg = LoadGraph(f_pickle_path)
	rg = LoadGraph(r_pickle_path)
	database.IsolateSubGraph(fg, ["face", "emotion"])
	set_trace()
	


"""
Old commands:
file_names = GetFileNamesInDirectory(maindir)
CreateEdgelist(maindir, file_names, outdir, 'forward_inference')
graph = ImportNcol(outdir+os.sep+'reverse_inference.txt')
fg.vs["names"]=file_names # Set the names of the vertices.
rg.vs["names"]=file_names # Set the names of the vertices.
SaveGraph(fg, f_pickle_path) # Pickle the forward graph.
SaveGraph(rg, r_pickle_path) # Pickle the reverse graph.
"""
