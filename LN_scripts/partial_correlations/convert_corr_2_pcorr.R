library(corpcor)

corr_mat_path <- paste('/Volumes/huettel/KBE.01/Analysis/Neurosynth/graph_analysis_data',
                '/NeurosynthMerge/merged_correlation/merged_correlation.csv', sep='')

pcorr_output_path <- paste('/Volumes/huettel/KBE.01/Analysis/Neurosynth/',
                'graph_analysis_data/NeurosynthMerge/merged_correlation/merged_pcorrelation.csv', sep='')

# Load correlation matrix.
corr_mat <- read.csv(corr_mat_path)

# Get rid of row labels.
corr_mat$X0.000 <- NULL

pcorr_mat <- cor2pcor(corr_mat)

# Save to csv.
write.table(pcorr_mat, file=pcorr_output_path, row.names=FALSE, col.names=FALSE, sep=",")
