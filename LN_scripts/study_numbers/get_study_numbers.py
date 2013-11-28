import os, sys
import cPickle

sys.path.append(os.path.realpath('..'))

from neurosynth.base.dataset import Dataset
from neurosynth.analysis import meta

""" Create a new Dataset instance from a database file and load features. 
This is basically the example from the quickstart in the README. 
Assumes you have database.txt and features.txt files in the current dir.
"""


try: 
	# Create Dataset instance from a database file.
	dataset = Dataset('database.txt')
except IOError:
	# Load features from file
	dataset.add_features('features.txt')
	# Pickle the Dataset to file so we can use Dataset.load() next time 
	# instead of having to sit through the generation process again.
	dataset.save('dataset.pkl')

import pdb; pdb.set_trace()

feature_names = dataset.get_feature_names()
number_of_studies = [len(dataset.get_ids_by_features(ids, threshold=0.001)) for ids in feature_names]
cPickle.dump(number_of_studies, open('/Volumes/huettel/KBE.01/Analysis/Neurosynth/SNAFiles/number_of_studies.p', 'wb'))
