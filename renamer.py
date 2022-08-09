import treeswift
import os
from alive_progress import alive_bar

wd = os.getcwd() + r'/pruned/'
os.chdir(wd)
print('Renaming Leaves')
with alive_bar(len(os.listdir(wd)), force_tty = True) as bar:
    for filename in os.listdir(wd):
        f = os.path.join(wd, filename)
        stree = treeswift.read_tree_newick(f)
        s_nodes = [node for node in stree.traverse_postorder()]
        for n in s_nodes:
            n.set_label(n.label.replace(" ", '_'))
        bar()
    print('Completed!')
