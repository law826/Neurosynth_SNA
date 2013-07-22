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

global searched_term_row
global listbox_row
searched_term_row = 3
listbox_row = 4


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
		self.searched_term_label = Label(self.root, text=self.entrystring)
		self.searched_term_label.grid(row=startingrow, columnspan=2)

	def SearchedTermUI(self, startingrow=None):
		self.SearchTermUI_startingrow=startingrow
		self.searched_term_label = Label(self.root, text="")
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
		self.clistbox.bind("<ButtonRelease-1>", self.UpdateNeighborsListBox)

	def NeighborsListBox(self, startingrow=None):	
		self.NeighborsLabel = Label(self.lbframe)
		self.NeighborsLabel["text"] = "Neighbors"
		self.NeighborsLabel.grid(row=0,column=1)
		self.nlistbox = Listbox(self.lbframe, width=40)
		self.nlistbox.grid(row=1,column=1)
		self.lbframe.grid(row=startingrow, column=0)

		#self.nlistbox.bind("<ButtonRelease-1>", self.SymptomListPressed)

	def UpdateNeighborsListBox(self, event=0):
		selected_index = self.clistbox.curselection()
		selected_concept = self.clistbox.get(selected_index)
		selected_vertex = self.DB.g.vs.find(term=selected_concept)
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
		self.nlistbox.grid(row=1, column=1)

	def SearchEntrySubmitted(self, event=0, list_clicked=False, selected_concept=None):
		if list_clicked:
			self.entrystring = selected_concept
			dneighbors, sneighbors = self.DB.FindNeighborsOfNode(self.entrystring)
		else:
			if self.entryWidget.get().strip() == "":
				tkMessageBox.showerror("Tkinter Entry Widget", "Enter a term")
			else:
				self.entrystring = self.entryWidget.get().strip()
				dneighbors, sneighbors = self.DB.FindNeighborsOfNode(self.entrystring)
				

		if (dneighbors == None) and (sneighbors == None):
			pass
		else:
			if self.DB.g.vs.find(name=self.entrystring)['type']=='Concepts':
				dneighbors = [self.entrystring]
			self.UpdateListBox(self.dlistbox, dneighbors, 1, 0)
			self.UpdateListBox(self.slistbox, sneighbors, 1, 1)
			self.UpdateSearchedTerm(startingrow=self.gui_element_dict[self.SearchedTermUI])
			self.entryWidget.delete(0, END)

	def ConceptsListPressed(self, event=0):
		selected_index = self.dlistbox.curselection()
		selected_concept = self.dlistbox.get(selected_index)
		self.SearchEntrySubmitted(list_clicked=True, selected_concept=selected_concept)
		self.ListFocus = "Concepts"

	def SymptomListPressed(self, event=0):
		selected_index = self.slistbox.curselection()
		selected_concept = self.slistbox.get(selected_index)
		self.SearchEntrySubmitted(list_clicked=True, selected_concept=selected_concept)
		self.ListFocus = "symptom"

	def ButtonsUI(self, startingrow=None):
		self.bottom_buttons_frame = Frame(self.root)
		button_labels = [
			"Reset",
			"View Graph",
			"Import",
			"Merge Items",
			"Debug Mode", 
			"Delete Item"
			]

		button_commands = [ 
			self.ResetButtonPressed,
			self.ViewGraphButtonPressed,
			self.ImportButtonPressed,
			self.MergeButtonPressed,
			self.DebugModeButtonPressed, 
			self.DeleteItem
			]

		for button_number, label in enumerate(button_labels):
			b = Button(self.bottom_buttons_frame, text=label, default="normal", command=button_commands[button_number]).pack()

		self.bottom_buttons_frame.grid(row=startingrow, columnspan=2)


	def ResetButtonPressed(self):
		self.ConceptsLabel.grid_forget()
		self.NeighborsLabel.grid_forget()
		self.dlistbox.grid_forget()
		self.slistbox.grid_forget()
		self.Listboxes()

	def ViewGraphButtonPressed(self):
		self.DB.g.write_svg("graph.svg", labels = "name", layout = self.DB.g.layout_kamada_kawai())
		os.system("open "+self.DB.save_path+os.sep+"graph.svg")

	def ImportButtonPressed(self):
		self.id.executeimport(self)

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
			self.ResetButtonPressed()
			tkMessageBox.showinfo("Term deleted", "%s has been deleted." %selected_concept)
		else:
			pass

def main():
	
	mainWindow = MainWindow()

if __name__ == '__main__':
    main()


### Utility scripts
## Delete all edges that are loops: STILL NEED TO TEST
# list_to_delete = [x.index for i, x in enumerate(self.DB.g.es) if self.DB.g.is_loop()[i]==True]
# self.DB.g.delete_edges(*list_to_delete)

