# import statements
import pandas as pd
import os
import treeswift
from alive_progress import alive_bar

wd = os.getcwd()
os.chdir(wd)
master = pd.read_csv('master_location_list.txt', sep = '\t')

wd = wd + r'/pruned/'
os.chdir(wd)
with alive_bar(len(os.listdir(wd)), force_tty = True) as bar:
    for filename in os.listdir(wd):
        f = os.path.join(wd, filename)
        stree = treeswift.read_tree_newick(f)
        s_nodes = [node.label for node in stree.traverse_leaves()]
        tree_df = pd.DataFrame(columns = ['id'], data = s_nodes)
        final = tree_df.merge(master, how = 'left', left_on = 'id', right_on = 'id')
        name = filename.replace('.tree','.txt')
        final.to_csv(name, sep = '\t', index = False)
        bar()
    print('Completed!')
