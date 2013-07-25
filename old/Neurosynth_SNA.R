library(igraph) 

# Load forward and reverse tables. 
forward_data_frame <- read.table('/Volumes/Huettel/KBE.01/Analysis/Neurosynth/Data/forward_inference.txt')
reverse_data_frame <- read.table('/Volumes/Huettel/KBE.01/Analysis/Neurosynth/Data/reverse_inference.txt')
colnames(forward_data_frame) <- c('ego', 'alter', 'PCorr')
head(forward_data_frame)
colnames(reverse_data_frame) <- c('ego', 'alter', 'PCorr')
head(reverse_data_frame)

# Check to see that the ego and alter columns match across the forward and reverse inference tables.
which(reverse_data_frame$ego != forward_data_frame$ego)
which(reverse_data_frame$alter != forward_data_frame$alter)

# Combine both forward and reverse tables. 
neurosynth_full_data_frame = cbind(forward_data_frame, reverse_data_frame$PCorr)
colnames(neurosynth_full_data_frame) = c('ego', 'alter', 'fCorr', 'rCorr')
head(neurosynth_full_data_frame)

# Load the attributes table and give matching vertex_number. 
attributes <- read.csv('/Volumes/Huettel/KBE.01/Analysis/Neurosynth/Data/attributes.txt', header=T)
attributes <- cbind(0:524, attributes)
colnames(attributes) = c('vertex_number', 'feature')

BConceptual50 <- read.csv('/Volumes/Huettel/KBE.01/Notes/Neurosynth_Correlations/Beam_Conceptual_50.txt', header=F)
colnames(BConceptual50) = c('feature')

############################### DATA PROCESSING
 
# Reduce to non-zero edges so that the edge list only contains actual ties of some type.
neurosynth_full_processed <- subset(neurosynth_full_data_frame, (fCorr > 0) | (rCorr > 0))
head(neurosynth_full_processed) 

## Reduce to only vertices of interest.
in_neuro_not_Beam <- setdiff(attributes$feature, BConceptual50$feature)
in_neuro_not_Beam <- data.frame(feature=in_neuro_not_Beam)
in_Beam_not_Neuro <- setdiff(BConceptual50$feature, attributes$feature)
in_Beam_not_Neuro <- data.frame(feature=in_Beam_not_Neuro)
vertex_numbers_in_neuro_not_Beam <- (merge(attributes, in_neuro_not_Beam, by = 'feature'))[,-1]
vertex_numbers_in_neuro_not_Beam <- data.frame(vertex_number=vertex_numbers_in_neuro_not_Beam)

neurosynth_full_processed <- subset(neurosynth_full_processed, ((!(ego %in% vertex_numbers_in_neuro_not_Beam$vertex_number)) & (!(alter %in% vertex_numbers_in_neuro_not_Beam$vertex_number))))
head(neurosynth_full_processed)

############################## END DATA PROCESSING

 
# Now we can import our data into a "graph" object using igraph's 
# graph.data.frame() function. Coercing the data into a graph
# object is what allows us to perform network-analysis techniques.
neurosynth_full_processed_graph <- graph.data.frame(neurosynth_full_processed) 
summary(neurosynth_full_processed_graph)
 
# By default, graph.data.frame() treats the first two columns of 
# a data frame as an edge list and any remaining columns as 
# edge attributes. Thus, the 232 edges appearing in the summary()
# output refer to the 232 pairs of vertices that are joined by 
# *any type* of tie. The tie types themselves are listed as edge 
# attributes.
 
# To get a vector of edges for a specific type of tie, use the 
# get.edge.attribute() function.
get.edge.attribute(neurosynth_full_processed_graph, 'rCorr')
get.edge.attribute(neurosynth_full_processed_graph, 'fCorr')


# If you would like to symmetrize the network, making all 
# asymmetric ties symmetric, use the as.undirected()
# function: 
neurosynth_full_processed_graph <- as.undirected(neurosynth_full_processed_graph, mode='collapse')
summary(neurosynth_full_processed_graph_symmetrized)
 
 
 
###
# 3. ADDING VERTEX ATTRIBUTES TO A GRAPH OBJECT
###
 
# One way to add the attributes to your graph object is to iterate
# through each attribute and each vertex. This means that we will
# add one attribute at a time to each vertex in the network.
#
# V(krack_full) returns a list of the IDs of each vertex in the 
# graph. names(attributes) returns a list of the column names in
# the attributes table. The double-for loop tells R to repeat the
# code between the brackets once for each attribute and once for
# each vertex.
for (i in 1:length(V(neurosynth_full_processed_graph))) {
    for (j in names(attributes)) {
        neurosynth_full_processed_graph <- set.vertex.attribute(neurosynth_full_processed_graph, 
                                           j, 
                                           index = i, 
                                           toString(attributes[as.numeric(V(neurosynth_full_processed_graph)$name[i]) + 1, j]))
    }
}

     

# A shorter way is to just read in attribute names when you
# create the graph object:
 
# First create a vector of vertex labels, in this case 1:n
#attributes = cbind(1:length(attributes[,1]), attributes)
 
#neurosynth_full_processed_graph <- graph.data.frame(d = forward_data_frame, 
 #                              vertices = attributes) 
 
# Note that we now have 'AGE,' 'TENURE,' 'LEVEL,' and 'DEPT'
# listed alongside 'name' as vertex attributes.
summary(neurosynth_full_processed_graph)
 
# We can see a list of the values for a given attribute for all of
# the actors in the network.
get.vertex.attribute(neurosynth_full_processed_graph, 'name')
get.vertex.attribute(neurosynth_full_processed_graph, 'vertex_number')
get.vertex.attribute(neurosynth_full_processed_graph, 'feature')
 
 
###
# 4. VISUALIZE THE NETWORKS
###
 
# We can use R's general-purpose plot() method to generate custom
# visualizations of the network.

# R only lets us look at one plot at a time.  To make our work easier
# we will save our plots as PDF files.  To jus create a plot execute 
# the code between the PDF function and "dev.off()".

# In order to save PDF files we must tell R where to put them.  We do
# this with the setwd() command.  You must put the full path to the
# folder where you will output the files here.

# In OS X you can get this information by selecting the folder, right
# clicking and selecting "Get Info."  The path is listed under "Where."

# In Windows you can get this information by selecting the folder, right
# clicking and selecting "Properties."  The path information is listed 
# "location".

# example: setwd("/Users/seanwestwood/Desktop/lab_1")
setwd("/Users/ln30/Dropbox/Research Assistants/Projects/Neurosynth/")
  

 
# forward only
forward_only <- delete.edges(neurosynth_full_processed_graph, 
    E(neurosynth_full_processed_graph)[get.edge.attribute(neurosynth_full_processed_graph,
    name = "fCorr") == 0])
forward_only_layout <- layout.fruchterman.reingold(forward_only)
#summary(forward_only)
pdf("conceptual_forward_only_000.pdf")
plot(forward_only, 
     vertex.label=V(forward_only)$feature,
     vertex.label.font=1,
     vertex.label.cex=0.5,
     main="Conceptual Forward Inference Network\n Thresh: R=0",
     frame=TRUE)
dev.off()

# reverse only
reverse_only <- delete.edges(neurosynth_full_processed_graph, 
    E(neurosynth_full_processed_graph)[get.edge.attribute(neurosynth_full_processed_graph,
    name = "rCorr") == 0])
reverse_only_layout <- layout.fruchterman.reingold(reverse_only)
#summary(forward_only)
pdf("conceptual_reverse_only_000.pdf")
plot(reverse_only, 
     vertex.label=V(reverse_only)$feature,
     vertex.label.font=1,
     vertex.label.cex=0.5,
     main="Conceptual Reverse Inference Network\n Thresh: R=0",
     frame=TRUE)
dev.off()



###########################################

# First, let's plot the network with all possible ties.
pdf("neurosynth_full_processed_graph.pdf")
plot(neurosynth_full_processed_graph)
dev.off()

# neurosynth_full_processed_graph_layout <- layout.fruchterman.reingold(neurosynth_full_processed_graph)
# pdf("Neurosynth_SNA.pdf") 
# plot(neurosynth_full_processed_graph, 
#      layout=neurosynth_full_processed_graph_layout, 
#      edge.arrow.size=1,
#      edge.width=1,
#      edge.arrow.width=1,
#      vertex.size=1, 
#      vertex.label.cex=1)
# dev.off()

# This is a bit of a jumble, so let's look at the networks for
# single edge types.

# plot(forward_only, 
#      layout=forward_only_layout, 
#      edge.arrow.size=1,
#      edge.width=1,
#      edge.arrow.width=1,
#      vertex.size=1, 
#      vertex.label.cex=1)
 
# friendship only
krack_friendship_only <- delete.edges(krack_full, 
    E(krack_full)[get.edge.attribute(krack_full, 
    name = "friendship_tie") == 0])
summary(krack_friendship_only)
pdf("1.3_Krackhardt_Friendship.pdf")
plot(krack_friendship_only)
dev.off()

# reports-to only
krack_reports_to_only <- delete.edges(krack_full, 
    E(krack_full)[get.edge.attribute(krack_full, 
    name = "reports_to_tie") == 0])
summary(krack_reports_to_only)
pdf("1.4_Krackhardt_Reports.pdf")
plot(krack_reports_to_only)
dev.off()
 
# Still kind of messy, so let's clean things up a bit. For 
# simplicity, we'll focus on reports_to ties for now.
 
# First, we can optimize the layout by applying the layout 
# algorithm to the specific set of ties we care about. Here 
# we'll use Fruchterman-Rheingold; other options are 
# described in the igraph help page for "layout," which 
# can be accessed by entering ?layout.

reports_to_layout <- layout.fruchterman.reingold(krack_reports_to_only)
pdf("1.5_Krackhardt_Reports_Fruchterman_Reingold.pdf")
plot(krack_reports_to_only, 
     layout=reports_to_layout)
dev.off()
 
# Now let's color-code vertices by department and clean up the 
# plot by removing vertex labels and shrinking the arrow size. 
dept_vertex_colors = get.vertex.attribute(krack_full,"DEPT")
colors = c('Black', 'Red', 'Blue', 'Yellow', 'Green')
dept_vertex_colors[dept_vertex_colors == 0] = colors[1]
dept_vertex_colors[dept_vertex_colors == 1] = colors[2]
dept_vertex_colors[dept_vertex_colors == 2] = colors[3]
dept_vertex_colors[dept_vertex_colors == 3] = colors[4] 
dept_vertex_colors[dept_vertex_colors == 4] = colors[5]

pdf("1.6_Krackhardt_Reports_Color.pdf") 
plot(krack_reports_to_only, 
    layout=reports_to_layout, 
    vertex.color=dept_vertex_colors, 
    vertex.label=NA, 
    edge.arrow.size=.5)
dev.off() 
# Now let's set the vertex size by tenure.
tenure_vertex_sizes = get.vertex.attribute(krack_full,"TENURE")

pdf("1.7_Krackhardt_Reports_Vertex_Size.pdf") 
plot(krack_reports_to_only, 
     layout=reports_to_layout, 
     vertex.color=dept_vertex_colors, 
     vertex.label=NA, 
     edge.arrow.size=.5,
     vertex.size=tenure_vertex_sizes
     )
dev.off() 
 
# Now let's incorporate additional tie types. We'll use the 
# layout generated by the reports-to ties but overlay the 
# advice and friendship ties in red and blue.

tie_type_colors = c(rgb(1,0,0,.5), rgb(0,0,1,.5), rgb(0,0,0,.5))
E(krack_full)$color[ E(krack_full)$advice_tie==1 ] = tie_type_colors[1]
E(krack_full)$color[ E(krack_full)$friendship_tie==1 ] = tie_type_colors[2]
E(krack_full)$color[ E(krack_full)$reports_to_tie==1 ] = tie_type_colors[3]
E(krack_full)$arrow.size=.5 
V(krack_full)$color = dept_vertex_colors
V(krack_full)$frame = dept_vertex_colors

pdf("1.8_Krackhardt_Overlayed_Ties.pdf")
plot(krack_full, 
     layout=reports_to_layout, 
     vertex.color=dept_vertex_colors, 
     vertex.label=NA, 
     edge.arrow.size=.5,
     vertex.size=tenure_vertex_sizes)
 
 
# Add a legend. Note that the plot window must be open for this to 
# work.
legend(1, 
       1.25,
       legend = c('Advice', 
                  'Friendship',
                  'Reports To'), 
       col = tie_type_colors, 
       lty=1,
       cex = .7)
dev.off() 
 
# Another option for visualizing different network ties relative 
# to one another is to overlay the edges from one tie type on the 
# structure generated by another tie type. Here we can use the
# reports-to layout but show the friendship ties:

pdf("1.9_Krackhardt_Overlayed_Structure.pdf")
plot(krack_friendship_only, 
     layout=reports_to_layout, 
     vertex.color=dept_vertex_colors, 
     vertex.label=NA, 
     edge.arrow.size=.5,
     vertex.size=tenure_vertex_sizes, 
     main='Krackhardt High-Tech Managers')
dev.off() 





#### OPTIONALS

# Analyze the distributions and correlation between the correlation coefficients of forward and reverse.
cor(neurosynth_full_data_frame$fCorr, neurosynth_full_data_frame$rCorr)
plot(neurosynth_full_data_frame$fCorr, neurosynth_full_data_frame$rCorr, xlab="Forward Inference Correlation Coefficient", ylab="Reverse Inference Correlation Coefficient")
hist(neurosynth_full_data_frame$fCorr, main="Distribution of Forward Inference Correlation Coefficients", xlab="Forward Inference Rs")
hist(neurosynth_full_data_frame$rCorr, main="Distribution of Reverse Inference Correlation Coefficients", xlab="Reverse Inference Rs")
 
###
# 5. EXPORT THE NETWORK
###
 
# The write.graph() function exports a graph object in various
# formats readable by other programs. There is no explicit
# option for a UCINET data type, but you can export the graph
# as a Pajek object by setting the 'format' parameter to 'pajek.'
# Note that the file will appear in whichever directory is set 
# as the default in R's preferences, unless you previously 
# changed this via setwd().
write.graph(krack_full, file='krack_full.dl', format="pajek")
 
# For a more general file type (e.g., importable to Excel),
# use the "edgelist" format. Note that neither of these will
# write the attributes; only the ties are maintained.
write.graph(krack_full, file='krack_full.txt', format="edgelist")