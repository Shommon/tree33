# tree33
This code will prune tree33 and perform ACCTRAN ACSR on all subtrees created.

Tree33 is one of the first child nodes of the original tree's root, and contains the largest number of descendants.

## R and Python Version
    Python 3.10
    R 4.1.2

## Important Packages
### Python
Please have these packages installed:

    pip install alive-progress

    pip install treeswift

    pip install -U dendropy

    pip install pandas


### R
Please have these packages installed:

    install.packages('phangorn')
    
    install.packages('ape')
    
    install.packages("svMisc")
    
    install.packages("tidyverse")

### Running Scripts
1. **Run pruner.py**, this prunes tree33 into 20,000 node trees by traversing a ladderized tree in postorder. Note: the progressbar may not fully progress to the end, if it overflows or underflows that is okay, as long as the code ends with "Complete!"
2. **Run renamer.py**, this fixes the node names from having spaces in the name. 
3. **Run location_create.py**, this creates location lists for each pruned subtree within the 'pruned/' folder
4. **Run reconstruct.R**, runs ACSR on trees in 'pruned/'

### Output
Final output should be within 'pruned/output/'
