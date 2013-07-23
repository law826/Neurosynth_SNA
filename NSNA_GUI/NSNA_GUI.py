#!/usr/bin/env python
# encoding: utf-8
"""
radiology_diagnoser.py

[] handle import file and merging
[] handle old matches from the merge window
[] connect higher order term to everything
[] order Neighbors in terms of best algorithm to get to specific Concepts
[] expand width of windows
[] entry box to merge two nodes in particular
[] figure out brackets
[] edit entry
[] fuzzy search
[] auto update Concepts and Neighbors list upon keystroke (implement fuzzy search)
[] clean up row management
[] make larger entry box
[] make a queue for stored dx and sx
[] make algorithm for stored dx and sx
[] figure out test for multiples for future developement
[] take care of capitalization
[] implement autofill
[] manage database (edit)
[] implement search (real use) of database

Started by LN on 7/4/13
"""
from __future__ import division
import os, sys, random as rand, tkMessageBox, tkFileDialog, cPickle, numpy as np, getpass, tkentrycomplete as tkcomp, re, nltk
from Tkinter import *
from pdb import *
from igraph import *

import basefunctions as bf
from db_for_gui_nsna import DataBaseForGUI
from mergewindow import MergeWindow
from importdata import ImportData
from subprocess import Popen, PIPE, STDOUT

class MainWindow:
	def __init__(self):
		self.MakeUI()

	def MakeUI(self):
		self.root = Tk()
		self.root.title("Neurosynth Network")
		self.DB = DataBaseForGUI(self) # Instantiated here at the end because of parent window issues for ask directory widget.
		self.mw = MergeWindow()
		self.id = ImportData()

		gui_elements = [self.SearchedTermUI,
						self.Listboxes,
						self.ButtonsUI
						]

		self.gui_element_dict = {}

		for startingrow, gui_element in enumerate(gui_elements):
			self.gui_element_dict[gui_element] = startingrow
			gui_element(startingrow=startingrow)
			
		self.root.mainloop()

	def Listboxes(self, startingrow=None):
		self.ConceptsListBox(startingrow=self.gui_element_dict[self.Listboxes])
		self.NeighborsListBox(startingrow=self.gui_element_dict[self.Listboxes])


	def DCWLabelEntryUI(self, startingrow):
		# Create a text frame to hold the text Label and the Entry widget
		self.DCWtextFrame = Frame(self.root)		
				
		self.DCWentryLabel = bf.Label(self.DCWtextFrame, "Enter a new Concepts followed by a comma and then Neighbors separated by commas.")
		try:
			self.DCWentry = bf.Entry(self.DCWtextFrame, self.ConceptsCharacterizationSubmitted, completion_list=self.DB.g.vs["name"])
		except KeyError:
			self.DCWentry = bf.Entry(self.DCWtextFrame, self.DiagnosisCharacterizationSubmitted, completion_list=[])

		self.DCWtextFrame.grid(row=startingrow, columnspan=2)

	def UpdateSearchedTerm(self, startingrow=None):
		startingrow = self.SearchTermUI_startingrow
		try:
			self.searched_term_label.grid_forget()
		except:
			pass
		self.searched_term_label = Label(self.root, text=self.DB.graph_mode+' Inference')
		self.searched_term_label.grid(row=startingrow, columnspan=2)

	def SearchedTermUI(self, startingrow=None):
		self.SearchTermUI_startingrow=startingrow
		self.searched_term_label = Label(self.root, text=self.DB.graph_mode+' Inference')
		self.searched_term_label.grid(row=startingrow, columnspan=2)

	def ConceptsListBox(self, startingrow=None):
		self.lbframe = Frame(self.root)
		# Label.
		self.ConceptsLabel = Label(self.lbframe)
		self.ConceptsLabel["text"] = "Concepts"
		self.ConceptsLabel.grid(row=0,column=0)

		# Listbox.
		self.clistbox = Listbox(self.lbframe, width=40)
		self.clistbox.grid(row=1,column=0)
		try: 
			for concept in self.DB.g.vs:
				self.clistbox.insert(END, concept["term"])
		except AttributeError:
		# If there are no items yet.
			pass
		self.clistbox.bind("<ButtonRelease-1>", self.ConceptsListPressed)

		try:
			self.NeighborsLabel2["text"] = self.selected_concept
			self.NeighborsLabel2.grid_forget()
			self.NeighborsLabel2.grid(row=2, column=0)
		except AttributeError:
			pass

	def NeighborsListBox(self, startingrow=None):	
		self.NeighborsLabel = Label(self.lbframe)
		self.NeighborsLabel["text"] = "Neighbors"
		self.NeighborsLabel.grid(row=0,column=1)
		self.nlistbox = Listbox(self.lbframe, width=40)
		self.nlistbox.grid(row=1,column=1)
		self.lbframe.grid(row=startingrow, column=0)
		self.NeighborsLabel2 = Label(self.lbframe)
		try:
			self.NeighborsLabel2["text"] = self.selected_neighbor
			self.NeighborsLabel2.grid_forget()
			self.NeighborsLabel2.grid(row=2, column=1)
		except AttributeError:
			pass
		self.nlistbox.bind("<ButtonRelease-1>", self.NeighborListPressed)

	def ConceptsListPressed(self, event=0):
		selected_index = self.clistbox.curselection()
		self.selected_concept = self.clistbox.get(selected_index)
		selected_vertex = self.DB.g.vs.find(term=self.selected_concept)
		self.nlistbox.delete(0, END)
		try: 
			self.DB.g.vs
			pair_list = [(neighbor['term'], self.DB.g[neighbor['name'], selected_vertex.index]) for neighbor in selected_vertex.neighbors()]
			pair_list.sort(key=lambda x: x[1])
			pair_list.reverse()
			for pair in pair_list:
				self.nlistbox.insert(END, "%s (%.3f)" %(pair[0], pair[1]))
		except AttributeError:
		# If there are no items yet.
			pass

		try:
			self.ConceptsLabel2.grid_forget()
		except AttributeError:
			pass

		self.ConceptsLabel2 = Label(self.lbframe)
		try:
			self.ConceptsLabel2["text"] = self.selected_concept
			self.ConceptsLabel2.grid(row=2, column=0)
		except AttributeError:
			pass
		self.nlistbox.grid(row=1, column=1)


	def NeighborListPressed(self, event=0):
		selected_index = self.nlistbox.curselection()
		self.selected_neighbor = self.nlistbox.get(selected_index).split(' ')[0]
		self.ListFocus = "symptom"
		try:
			self.NeighborsLabel2["text"] = self.selected_neighbor
			self.NeighborsLabel2.grid_forget()
			self.NeighborsLabel2.grid(row=2, column=1)
		except AttributeError:
			pass
		self.nlistbox.bind("<ButtonRelease-1>", self.NeighborListPressed)

	def ButtonsUI(self, startingrow=None):
		self.bottom_buttons_frame = Frame(self.root)
		button_labels = [
			"View Brain Overlay",
			"Forward/Reverse Mode",
			"View Graph",
			"Merge Items",
			"Debug Mode", 
			"Delete Item"
			]

		button_commands = [ 
			self.ViewBrainOverlayButtonPressed,
			self.ForwardReverseButtonPressed,
			self.ViewGraphButtonPressed,
			self.MergeButtonPressed,
			self.DebugModeButtonPressed, 
			self.DeleteItem
			]

		for button_number, label in enumerate(button_labels):
			b = Button(self.bottom_buttons_frame, text=label, default="normal", command=button_commands[button_number]).pack()

		self.bottom_buttons_frame.grid(row=startingrow, columnspan=2)

	def ForwardReverseButtonPressed(self):
		if self.DB.graph_mode == 'Forward':
			self.DB.graph_mode = 'Reverse' 
		elif self.DB.graph_mode == 'Reverse':
			self.DB.graph_mode = 'Forward'
		self.DB.LoadGraph()
		self.UpdateSearchedTerm()
		self.UpdateListboxes()

	def ViewGraphButtonPressed(self):
		self.DB.g.write_svg("graph.svg", labels = "name", layout = self.DB.g.layout_kamada_kawai())
		os.system("open "+self.DB.save_path+os.sep+"graph.svg")

	def ViewBrainOverlayButtonPressed(self):
		image_maindir = os.sep.join(['/Volumes', 'huettel', 'KBE.01',  'Analysis', 'Neurosynth', 'neurosynthgit', 'results'])
		image_dir = os.sep.join([image_maindir, self.DB.graph_mode+'_inference_unthresh_z'])
		if self.DB.graph_mode == 'Forward':
			image_name1 = '_%s_pAgF_z.nii.gz' % self.selected_concept
			image_name2 = '_%s_pAgF_z.nii.gz' % self.selected_neighbor
		elif self.DB.graph_mode == 'Reverse':
			image_name1 = '_%s_pFgA_z.nii.gz' % self.selected_concept
			image_name2 = '_%s_pFgA_z.nii.gz' % self.selected_neighbor

		standard_brain_path = 'fslview ${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz'

		image_path1 = os.sep.join([image_dir, image_name1])
		image_path2 = os.sep.join([image_dir, image_name2])
		lookup_table1 = '-l "Red-Yellow"'
		lookup_table2 = '-l "Blue-Lightblue"'

		shell_command = '%s %s %s %s %s' %(standard_brain_path, image_path1, lookup_table1, image_path2, lookup_table2)
		print shell_command

		
		event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		output = event.communicate()


	def MergeButtonPressed(self):
		self.mw.ExecuteMerge(self)

	def DebugModeButtonPressed(self):
		import pdb; pdb.set_trace()

	def DeleteItem(self):
		selected_concept = self.entrystring
		result = tkMessageBox.askquestion("Delete", "Are you sure you want to delete %s?" %selected_concept, icon='warning')
		if result == 'yes':
			vertex_index = self.DB.g.vs.find(name=selected_concept).index
			self.DB.g.delete_vertices(vertex_index)
			self.DB.SaveGraph()
			self.UpdateListboxes()
			tkMessageBox.showinfo("Term deleted", "%s has been deleted." %selected_concept)
		else:
			pass

	def UpdateListboxes(self):
		self.clistbox.pack_forget()
		self.nlistbox.pack_forget()
		self.lbframe.grid_forget()
		self.Listboxes(startingrow=self.gui_element_dict[self.Listboxes]) # This is the combination of forming both boxes in one function.


def main():
	
	mainWindow = MainWindow()

if __name__ == '__main__':
    main()


### Utility scripts
## Delete all edges that are loops: STILL NEED TO TEST
# list_to_delete = [x.index for i, x in enumerate(self.DB.g.es) if self.DB.g.is_loop()[i]==True]
# self.DB.g.delete_edges(*list_to_delete)

