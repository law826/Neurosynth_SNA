#!/usr/bin/env python
# encoding: utf-8
"""
Neurosynth_SNA.py

"""
from __future__ import division
import os, sys, getpass
import random as rand
import cPickle
import numpy as np
from igraph import *
from pdb import *

def ImportData(file):
	graph = Graph.Read_Edgelist(file)
	return graph

def VisualizeData():
	pass











def main():
	pass

if __name__ == '__main__':
	main()