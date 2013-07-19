from __future__ import division
import os
import sys
import random as rand
import cPickle 
import numpy as np
import getpass
import nltk
from pdb import *
from igraph import *
import pickle
from Tkinter import *
import basefunctions as bf
import unittest

class CategorizeNodesGUI:
	def __init__(self, list_of_nodes, save_file):
		"""
		Launches a GUI and iterates through nodes so that they can be categorized under various types.
		Input: (1) list of nodes (2) save path.
		Output: (1) a pickle in the current directory that represents a list of tuples of categorizations
		(i.e. (term, type))
		"""
		self.editmode = False
		self.list_of_nodes = list_of_nodes
		self.save_file = save_file
		self.LoadTupleFile()
		self.MakeUI()

	def MakeUI(self):
		self.root = Tk()
		self.root.title("Ideas Generator")
		self.root["padx"] = 40
		self.root["pady"] = 20

		self.dt_frame = Frame(self.root)
		self.label = bf.Label(self.root, "Please Categorize:")
		self.dt_frame.pack()
		self.DisplayTerm()
		self.Buttons()		
		self.lbframe = Frame(self.root)
		self.MakeListBox()
		self.lbframe.pack()
		self.root.mainloop()

	def Buttons(self):
		buttonFrame = Frame(self.root)
		b1 = Button(buttonFrame, text='brain', command = lambda: self.AssignType('brain')).pack(side = LEFT)
		b1 = Button(buttonFrame, text='concept', command = lambda: self.AssignType('concept')).pack(side = LEFT)
		buttonFrame.pack()

	def AssignType(self, button):
		if self.editmode == True:
			index_to_edit = next(index for index, pair in enumerate(self.tuple_list) if pair[0] == self.node_to_eval)
			self.tuple_list[index_to_edit] = (self.node_to_eval, button)

		elif self.node_to_eval != "No more terms to evaluate!":
			self.tuple_list.append((self.node_to_eval, button))
		
		self.SaveTupleFile()
		self.LoadTupleFile()
		self.UpdateDisplayTerm()
		self.UpdateListBox()
		self.editmode = False

	def DisplayTerm(self):
		if self.editmode == True:
			pass
		else:
			try: 
				self.node_to_eval = next(node for node in self.list_of_nodes if node not in self.saved_pairs[0])
			except StopIteration:
				self.node_to_eval = "No more terms to evaluate!"
			except IndexError:
				self.node_to_eval = next(node for node in self.list_of_nodes)

		self.dt = bf.Label(self.dt_frame, self.node_to_eval)

	def UpdateDisplayTerm(self):
		self.dt.pack_forget()
		self.DisplayTerm()

	def MakeListBox(self):	
		self.b0 = Button(self.lbframe, text = "Edit Type", command = lambda: self.EditTypeButtonPressed(0))
		self.b0.pack()
		self.listbox = Listbox(self.lbframe, width=40)
		self.listbox.pack()

		try: 
			for pair in self.tuple_list:
				self.listbox.insert(END, pair)
		except AttributeError:
		# If there are no items yet.
			pass

	def EditTypeButtonPressed(self, button_index):
		selected_index = self.listbox.curselection()
		selected_concept = self.listbox.get(selected_index)

		self.editmode = True
		self.node_to_eval = selected_concept[0]
		self.UpdateDisplayTerm()
		self.UpdateListBox()

	def UpdateListBox(self):
		self.listbox.pack_forget()
		self.b0.pack_forget()
		self.MakeListBox()

	def LoadTupleFile(self):
		try:
			self.tuple_list = pickle.load(open(self.save_file, 'rb'))
		except IOError:
			self.tuple_list = []
		self.saved_pairs = map(list, zip(*self.tuple_list))

	def SaveTupleFile(self):
		pickle.dump(self.tuple_list, open(self.save_file, 'wb'))

	def main():
		
		cv = CategorizeNodes()

class CNBridge:
	"""
	Take the picke output from CategorizeNodesGUI and apply it to existing graph.
	This only applies to the attribute = 'type' and 'term' at this point. 
	"""
	def __init__(self, graph, pickle_path):
		self.save_file = pickle_path
		self.g = graph
	
	def LoadPickle(self):
		self.tuple_list = pickle.load(open(self.save_file, 'rb'))
		self.saved_pairs = map(list, zip(*self.tuple_list))
		for i, pair in enumerate(self.tuple_list):
			self.node = self.g.vs.find(term=(self.saved_pairs[0][i]))
			self.node['type'] = self.saved_pairs[1][i]

if __name__ == '__main__':
	main()

