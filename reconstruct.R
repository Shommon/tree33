# PLEASE INSTALL THESE PACKAGES
#install.packages('phangorn')
#install.packages('ape')
#install.packages("svMisc")
#install.packages("tidyverse")
print('Setting Up Libraries...')
library(phangorn)
library(ape)
library(svMisc)
library(tidyverse)

setwd(getwd())

#ancestral character state reconstruction using parsimony
ancestral_reconstruction <- function(phylo, locdat){
  ancestors_loc <- ancestral.pars(phylo, locdat, type = "ACCTRAN") #without cost matrix specified: Fitch algorithm
  
  n_tips <- Ntip(phylo) #number of tips
  n_nodes <- length(unique(phylo$edge[,1])) #number of internal nodes
  n <- n_tips + n_nodes
  
  all_loc <- levels(locdat)
  node_locs <- vector(mode="character", length=n)
  
  for (i in 1:n) {
    node_locs[i] <- all_loc[which(ancestors_loc[[i]] == max(ancestors_loc[[i]]))][1]
  }
  
  # add internal node IDs
  #node_label <- paste("intNode", seq(1, n_nodes), sep="")
  #phylo$node.label <- node_label
  
  # create annotation
  node_annotation <- data.frame(label=c(phylo$tip.label, phylo$node.label), location=node_locs)
  
  return(list(tree=phylo, annotation=node_annotation))
}

## Saving Tree
save_tree <- function(result, filename){
  write.tree(result$tree, paste(filename,".phy", sep=""))
  # write.tree replaces spaces in sequence names by underscores - do the same with annotation file
  result$annotation$label <- gsub(" ", "_", result$annotation$label)
  write.table(result$annotation, paste(filename, ".annotation.txt", sep=""), quote=FALSE, row.names=FALSE, sep="\t")
}
print('Functions Loaded')



#Loop
n <- length(list.files('pruned/',pattern="tree$", full.names = TRUE, recursive = TRUE))
#Progress Bar
print('Starting ACSR...')
for (x in 1:n){
progress(n,x)
treename <- paste('pruned/tree33_',x,'.tree', sep='')
locations <- paste('pruned/tree33_',x,'.txt', sep='')
tree <- read.tree(file=treename)

location_info <- read.table(locations, header=TRUE, sep="\t")
#observed locations
tipdata <- as.matrix(location_info$location)
row.names(tipdata) <- location_info$id

#save observed locations in phyDat format
all_locs <- unique(tipdata)
locdat <- phyDat(tipdata, type="USER", levels=all_locs)

## Final Reconstruction
ancestral <- ancestral_reconstruction(tree, locdat)
outfile <- paste('output/final',x , sep='')
save_tree(ancestral, outfile)
}
print('ACSR Completed! files in output folder')
