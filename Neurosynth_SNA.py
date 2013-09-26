#!/usr/bin/env python
# encoding: utf-8
"""
[] paths has changed to a class
[] import the neurosynth code for counting study numbers
[] be careful with naming variable "list"
[] path notation has been changed.
[] get merge list from everyone
[] run the new list of merged terms
[] rerun all the code up to this point
[] clean up code from listclass migration
[] encode number of studies
[] research page rank
[] get cairo working
[] make functionality for starting from the beginning again.
[] test whether current import protocol works
[] add functionality for windowsj
[] perform centrality measures on the data
[] incorporate new data
[] look at correlations between similar items and figure out merging
"""
from __future__ import division
import database
from pdb import *
import os, sys, getpass, random as rand, cPickle, numpy as np
import re

from ListClass import ListClass

try:
    from igraph import *
except ImportError:
    raise ImportError, "The igraph module is required to run this program."


class Paths():   
    def __init__(self):

        """
        Sets the relevant paths for windows, linux, and mac systems.

        Paths (common usages):
            - maindir: Directory where the numpy save files are (single columns which serve as inputs creating the edgelist found in importdir).
            - outdir: Main output directory where graph pickles and graphical statistics (e.g. centrality) are stored.
            - importdir: Where the edgelists are after processing of the single column files from outdir.
            - *pickle_path: Paths of the forward and reverse pickles.
            - *edgelist: Exist paths of the edgelists from importdir.
        """
        if sys.platform == "darwin":
            self.maindir = os.path.join('/Volumes', 'huettel', 'KBE.01',  'Analysis', 'Neurosynth', 'correlations_raw_data', 'ForwardResults')
            self.outdir  = os.path.join('/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data')
            self.importdir  = os.path.join('/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'correlations_raw_data')
            self.pickle_path = os.path.join('/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles')
            self.r_pickle_path = os.path.join('/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles', 'reverse_graph.p')
            self.f_pickle_path = os.path.join('/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles', 'forward_graph.p')
            self.git_path = os.path.join('/Volumes', 'huettel', 'KBE.01', 'Analysis', 'Neurosynth', 'neurosynthgit')
        elif sys.platform == "win32":
            self.maindir = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'correlations_raw_data', 'ForwardResults')
            self.outdir  = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data')
            self.importdir  = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'Data')
            self.pickle_path = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles')
            self.r_pickle_path = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles', 'reverse_graph.p')
            self.f_pickle_path = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles', 'forward_graph.p')
            self.git_path = os.path.join('M:', 'KBE.01', 'Analysis', 'Neurosynth', 'neurosynthgit')
        elif sys.platform == "linux2":
            self.username=getpass.getuser()
            self.maindir = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'correlations_raw_data', 'ForwardResults')
            self.outdir  = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data')
            self.importdir  = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'correlations_raw_data')
            self.pickle_path = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles')
            self.r_pickle_path = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles', 'reverse_graph.p')
            self.f_pickle_path = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'graph_analysis_data', 'pickles', 'forward_graph.p')
            self.git_path = os.path.join('/home', username, 'experiments', 'KBE.01', 'Analysis', 'Neurosynth', 'neurosynthgit')

        self.forward_inference_edgelist = os.path.join(self.outdir, "forward_inference.txt")
        self.reverse_inference_edgelist = os.path.join(self.outdir, "reverse_inference.txt")

class NeurosynthMerge:
    def __init__(self, thesaurus, npath, outdir, test_mode=False):
        """
        Generates a new set of images using the neurosynth repository combining across terms in a thesarus.

        Args:
            - thesaurus: A list of tuples where:[('term that will be the name of the file', 'the other term', 'expression combining the terms')]
                    - the last expression is alphanumeric and separated by: (& for and) (&~ for andnot) (| for or) 
            - npath: directory where the neurosynth git repository is locally on your machine (https://github.com/neurosynth/neurosynth)
            - outdir: directory where the generated images will be saved
            - test_mode: when true, the code will run an abridged version for test purposes (as implemented by test.Neurosynth.py)
        """
        self.thesaurus = thesaurus
        self.npath = npath
        self.outdir = outdir

        self.import_neurosynth_git()
        from neurosynth.analysis import meta

        # Take out first two terms from the feature_list and insert the third term from the tuple.
        for triplet in thesaurus:
            self.feature_list = [feature for feature in self.feature_list if feature not in triplet]
            self.feature_list.append(triplet[-1])

        # This makes an abridged version of feature_list for testing purposes. 
        if test_mode:
            self.feature_list = [triplet[-1] for triplet in thesaurus]

        # Run metanalyses on the new features set and save the results to the outdir.
        for feature in self.feature_list:
            self.ids = self.dataset.get_ids_by_expression(feature, threshold=0.001)
            ma = meta.MetaAnalysis(self.dataset, self.ids)

            # Parse the feature name (to avoid conflicts with illegal characters as file names)
            regex = re.compile('\W+')
            split = re.split(regex, feature)
            feat_fname = split[0] 

            # Save the results (many different types of files)
            ma.save_results(self.outdir+os.sep+feat_fname)

    def import_neurosynth_git(self):
        # Add the appropriate neurosynth git folder to the python path. 
        sys.path.append(self.npath)
        from neurosynth.base.dataset import Dataset
        from neurosynth.analysis import meta

        # Try to load a pickle if it exists. Create a new dataset instance if it doesn't.
        try:
            self.dataset = cPickle.load(open(self.npath+os.sep+'data/dataset.pkl', 'rb'))
        except IOError:
        # Create Dataset instance from a database file.
            self.dataset = Dataset(self.npath+os.sep+'data/database.txt')

        # Load features from file
        self.dataset.add_features(self.npath+os.sep+'data/features.txt')

        # Get names of features. 
        self.feature_list = self.dataset.get_feature_names()

        #ids = self.dataset.get_ids_by_expression('recollection', threshold=0.001); print len(ids)
        #import pdb; pdb.set_trace()

class ArticleAnalysis():
    """
    Performs calcluations related to number of articles associated with a term.
    [] Write code that will assign the Jaccard to a given edge.
    """
    def __init__(self, npath):
        """
        Sets the neurosynthgit directory and loads a dataset instance that was previously created.
        """
        self.npath = npath
        sys.path.append(self.npath)
        from neurosynth.base.dataset import Dataset
        from neurosynth.analysis import meta
        ns_pickle = os.path.join(self.npath, 'data/dataset.pkl')
        self.dataset = cPickle.load(open(ns_pickle, 'rb'))

    def CalculateNumberofArticles(self, term):
        """
        Takes in a term and returns the number of studies associated with the term.
        """
        self.term = term
        ids = self.dataset.get_ids_by_expression(self.term, threshold=0.001)
        num_ids = len(ids)
        return num_ids

    def CalculateJaccard(self, term1, term2):
        unique_ex1 = term1 + '&~' + term2
        unique_ex2 = term2 + '&~' + term1
        union = term1 + '|' + term2
        intersection = term1 + '&' + term2

        unique_stud1 = self.CalculateNumberofArticles(unique_ex1)
        unique_stud2 = self.CalculateNumberofArticles(unique_ex2)
        union_stud = self.CalculateNumberofArticles(union)
        intersection_stud = self.CalculateNumberofArticles(intersection)

        jaccard = intersection_stud/union_stud
        return jaccard

    def AssignJaccardsToGraph(self, graph, gr_out_pth):
        """
        Takes a graph and assigns the Neurosynth Jaccard index for the number of studies relevant terms appear in.
            Args:
                - graph
                - gr_out_pth: path for the pickle of the new modified graph.
        """
        # Dissection of elements of the graph.
        edge_tuple_list = [e.tuple for e in graph.es]
        edge_term_tuple_list = [(graph.vs[pair[0]]['term'], graph.vs[pair[1]]['term']) for pair in edge_tuple_list]

        # Calculation of the jaccards of each edge.
        jaccard_list = []
        for i, pair in enumerate(edge_term_tuple_list):
            jaccard = self.CalculateJaccard(pair[0], pair[1])
            jaccard_list.append(jaccard)

        # Assigning the jaccards to the graph and saving.
        graph.es['article_jaccard'] = jaccard_list
        Graph.write_pickle(graph, gr_out_pth)

    def OutputJaccardsAndWeightsToFiles(self, graph_pickle, directory):
        """
        Takes a graph that already has the number of studies jaccard attribute and outputs files appropriate 
            to create a jaccard vs. weight scatter plot.
        """
        graph = Graph.Read_Pickle(graph_pickle)
        with open(os.path.join(directory, 'jaccard.txt'), 'w') as f:
            for i, jaccard in enumerate(graph.es['article_jaccard']):
                tuple_index = graph.es[i].tuple # This is the indexed term of the relevant vertices of the given edge.
                first_vertex = graph.vs[tuple_index[0]]["term"]
                second_vertex = graph.vs[tuple_index[1]]["term"]
                brain_weight = graph.es[i]["weight"]
                f.write('%s-%s,%s,%s\n' % (first_vertex, second_vertex, brain_weight, jaccard))










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

def LoadPickle(pickle_path):
    # In contrast to the above function, this just loads a pickle that does not have to be a graph.
    loaded_pickle = cPickle.load(open(pickle_path, 'rb'))
    return loaded_pickle

def StripName(graph, rawterms): 
    """
    input: nameless graph, nonstripped list of terms(separated by underscores)
    output: graph of stripped terms (name of attribute= "term")
    Ex. list_rawterms = rg.vs["term"]
        rg = StripName(rg, list_rawterms)
    """
    graph.vs["term"]=rawterms # Set the names of the vertices.
    graph.vs["term"]=[x.split('_')[1] for x in graph.vs["term"]]
    return graph

def ModifySubGraph(graph):
    """
    input: graph of analysis (fg or rg)
    output: network image
    modifies graph into subgraph given a list (sub_list_concept) and creates network image
    """
    if graph == fg:
        listclass = ListClass()
        sub_list_concept = listclass.sub_Beam_concepts
        ns = LoadPickle('M:/KBE.01/Analysis/Neurosynth/graph_analysis_data/pickles/number_of_studies.p')
        graph.vs["numberofstudies"] = ns #creates attribute for number of studies
        npns = np.array(ns) #creates array of number of studies
        nsl = np.log10(npns) #calculates log of number of studies
        graph.vs["log"] = nsl*8 #multiplies constant to create attribute "log"
        sfgc = database.IsolateSubGraph(graph, sub_list_concept, "term") # creates sub graph from main graph rg
        index_to_delete = [edge.index for edge in sfgc.es.select(weight_lt=0.8)] # creates threshold by selecting edges lower than a certain weight
        sfgc.delete_edges(index_to_delete) #deletes selected edges
        visual_style = {} #sets method of modifying graph characteristics
        visual_style ["vertex_label"]= sfgc.vs["term"] # labels the vertices
        visual_style ["vertex_label_dist"] = 2 # specifies the distance between the labels and the vertices
        visual_style ["vertex_size"] = sfgc.vs["log"] # specifies size of vertex_size
        visual_style["bbox"] = (700,700) #sets dimensions for the box layout
        visual_style["margin"] = 60
        plot(sfgc, **visual_style) # creates the changes
        #plot (sfgc, outdir+os.sep+ "forward_sub_graph_concept", **visual_style) # creates the changes
        #SaveGraph(srgc, outdir+os.sep+"sub_reverse_graph_concept_test") #saves graph in outdir
    elif graph == rg:
        listclass = ListClass()
        sub_list_concept = listclass.sub_Beam_concepts
        ns = LoadPickle('M:/KBE.01/Analysis/Neurosynth/graph_analysis_data/pickles/number_of_studies.p')
        graph.vs["numberofstudies"] = ns #creates attribute for number of studies
        npns = np.array(ns) #creates array of number of studies
        nsl = np.log10(npns) #calculates log of number of studies
        graph.vs["log"] = nsl*8 #multiplies constant to create attribute "log"
        srgc = database.IsolateSubGraph(graph, sub_list_concept, "term") # creates sub graph from main graph rg
        index_to_delete = [edge.index for edge in srgc.es.select(weight_lt=0.2)] # creates threshold by selecting edges lower than a certain weight
        srgc.delete_edges(index_to_delete) #deletes selected edges
        visual_style = {} #sets method of modifying graph characteristics
        visual_style ["vertex_label"]= srgc.vs["term"] # labels the vertices
        visual_style ["vertex_label_dist"] = 1.0 # specifies the distance between the labels and the vertice
        visual_style ["vertex_size"] = srgc.vs["log"] # specifies size of vertex_size
        visual_style["bbox"] = (750,750) #sets dimensions for the box layout
        visual_style["margin"] = 60
        plot(srgc, **visual_style) # creates the changes
        #plot (sfgc, outdir+os.sep+ "forward_sub_graph_concept", **visual_style) # creates the changes
        #SaveGraph(srgc, outdir+os.sep+"sub_reverse_graph_concept") #saves graph in outdir

def SaveCentrality(graph, type, file_name):
    """
    saves a list of tuples to csv file
    graph- graph used to calculate centrality
    type- what type of centrality being calculated (degree, eigenvector, betweenness, distance)
    file_name- the name of the file you would like created
    """
    import csv
    list= database.NodesInOrderOfCentrality(graph, type)
    with open(outdir+os.sep+file_name+'.csv', 'wb') as result:
        writer = csv.writer(result, dialect= 'excel')
        writer.writerows(list)

class NeurosynthMerge:
    def __init__(self, thesaurus, npath, outdir, test_mode=False):
        """
        Generates a new set of images using the neurosynth repository combining across terms in a thesarus.

        Args:
            - thesaurus: A list of tuples where:[('term that will be the name of the file', 'the other term', 'expression combining the terms')]
                    - the last expression is alphanumeric and separated by: (& for and) (&~ for andnot) (| for or) 
            - npath: directory where the neurosynth git repository is locally on your machine (https://github.com/neurosynth/neurosynth)
            - outdir: directory where the generated images will be saved
            - test_mode: when true, the code will run an abridged version for test purposes (as implemented by test.Neurosynth.py)
        """
        self.thesaurus = thesaurus
        self.npath = npath
        self.outdir = outdir

        self.import_neurosynth_git()
        from neurosynth.analysis import meta

        # Take out first two terms from the feature_list and insert the third term from the tuple.
        for triplet in thesaurus:
            self.feature_list = [feature for feature in self.feature_list if feature not in triplet]
            self.feature_list.append(triplet[-1])

        # This makes an abridged version of feature_list for testing purposes. 
        if test_mode:
            self.feature_list = [triplet[-1] for triplet in thesaurus]

        # Run metanalyses on the new features set and save the results to the outdir.
        for feature in self.feature_list:
            self.ids = self.dataset.get_ids_by_expression(feature, threshold=0.001)
            ma = meta.MetaAnalysis(self.dataset, self.ids)

            # Parse the feature name (to avoid conflicts with illegal characters as file names)
            regex = re.compile('\W+')
            split = re.split(regex, feature)
            feat_fname = split[0] 

            # Save the results (many different types of files)
            ma.save_results(self.outdir+os.sep+feat_fname)

    def import_neurosynth_git(self):
        # Add the appropriate neurosynth git folder to the python path. 
        sys.path.append(self.npath)
        from neurosynth.base.dataset import Dataset
        from neurosynth.analysis import meta

        # Try to load a pickle if it exists. Create a new dataset instance if it doesn't.
        try:
            self.dataset = cPickle.load(open(self.npath+os.sep+'data/dataset.pkl', 'rb'))
        except IOError:
        # Create Dataset instance from a database file.
            self.dataset = Dataset(self.npath+os.sep+'data/database.txt')

        # Load features from file
        self.dataset.add_features(self.npath+os.sep+'data/features.txt')

        # Get names of features. 
        self.feature_list = self.dataset.get_feature_names()

        #ids = self.dataset.get_ids_by_expression('recollection', threshold=0.001); print len(ids)
        #import pdb; pdb.set_trace()

"""
saves a list of tuples to csv file
graph- graph used to calculate centrality
type- what type of centrality being calculated (degree, eigenvector, betweenness, distance)
file_name- the name of the file you would like created
"""

####### Statistics
def VisualizeGraph(graph, outpath):
    graph.write_svg(outpath, labels = "term", layout = graph.layout_kamada_kawai())

def CalculateBetweennessCentrality(graph):
    pass



"""
Start of specific user commands.

To do list:


""" 
if __name__ == '__main__':
    paths = Paths() # Paths is a now a class object, and the way to access to paths is demonstrated below. 
    fg = LoadGraph(paths.f_pickle_path)
    rg = LoadGraph(paths.r_pickle_path)
    srgc = LoadGraph(paths.pickle_path+os.sep+'sub_reverse_graph_concept.p')
    vsrgc = srgc.community_fastgreedy(weight = "weights")
    plot(vsrgc)
    
    
    set_trace()


"""
Old commands:
file_names = GetFileNamesInDirectory(maindir)
CreateEdgelist(maindir, file_names, outdir, 'forward_inference')
graph = ImportNcol(outdir+os.sep+'reverse_inference.txt')
fg.vs["term"]=file_names # Set the names of the vertices.
rg.vs["term"]=file_names # Set the names of the vertices.
SaveGraph(fg, f_pickle_path) # Pickle the forward graph.
SaveGraph(rg, r_pickle_path) # Pickle the reverse graph.
os.system("start "+ "test_graph") #opens igraph in browser for windows
fg.to_undirected(mode="collapse", combine_edges= "max") #makes graph without direction, thus A to B is same as B to A
rg.to_undirected(mode="collapse", combine_edges= "max")
fg = database.StripLoops(fg) # Removes loops (values with itself such as A to A, etc.)
rg = database.StripLoops(rg)

saves as list of terms
list= fg.vs["term"]
    with open('list_term.csv', 'wb') as result:
        writer = csv.writer(result, dialect= 'excel')
        for x in list:
            writer.writerow([x])
    

save functions for list of tuples to csv:
# import csv
# test_list= database.NodesInOrderOfCentrality(fg, "degree")
# result = open("testfile.csv", 'wb')
# writer = csv.writer(result, dialect = 'excel')
# writer.writerows(test_list)

creating betweenness centrality measures to compare with Beam et al
srgc = LoadPickle('M:/KBE.01/Analysis/Neurosynth/graph_analysis_data/pickles/sub_reverse_graph_concept.p')
    ng= srgc
    ng.es["weight"] = [x+1 for x in ng.es["weight"]]
    bng= database.NodesInOrderOfCentrality(ng, 'betweenness')
    srngc= database.NodesInOrderOfCentrality(srgc, 'betweenness')
    import csv
    one_list= bng
    zero_list= srngc
    with open('betweenness_test.csv', 'wb') as result:
        writer = csv.writer(result, dialect= 'excel')
        for x in zero_list:
            writer.writerow([x])


creating nodes that are different sizes based on numberofstudies
 ns = LoadPickle('M:/KBE.01/Analysis/Neurosynth/graph_analysis_data/pickles/number_of_studies.p')
 rg.vs["numberofstudies"] = ns #creates attribute for number of studies
 npns = np.array(ns) #creates array of number of studies
 nsl = np.log10(npns) #calculates log of number of studies
 rg.vs["log"] = nsl*8 #multiplies constant to create attribute "log"
 ModifySubGraph(rg)
    

"""


