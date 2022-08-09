from alive_progress import alive_bar
import treeswift
import dendropy
import pandas as pd
import os

wd = os.getcwd()
os.chdir(wd)
tree = dendropy.Tree.get(path = 'tree33_NEW.tree', schema = 'newick')
stree = treeswift.read_tree_dendropy(tree)
s_node_list = [node for node in stree.traverse_postorder(leaves=False)]
filename_df = pd.DataFrame(columns = ['node', 'file_name'])

### WHILE LOOP ###
i = 0
num = 1
length = len(s_node_list)
prune = True

print('Pruning Trees')
with alive_bar(422, force_tty = True) as bar:
    while prune == True:
        st1 = stree.extract_subtree(s_node_list[i])
        if st1.num_nodes() in range(20000,40000):
            node = s_node_list[i]
            outfile = 'pruned/tree33_' + str(num) + '.tree'
            filename_df.loc[num-1] = [node.label] + [outfile]
            st1.write_tree_newick(filename = outfile, hide_rooted_prefix=True)
            bar()

            top_node = tree.find_node_with_label(node.label)
            bottom_node = top_node.parent_node
            tree.prune_subtree(top_node,suppress_unifurcations=False) #Dendropy

            top_node = dendropy.Node(label = node.label)
            bottom_node.add_child(top_node)

            stree = treeswift.read_tree_dendropy(tree)
            s_node_list = [x for x in stree.traverse_postorder(leaves=False)]
            length = len(s_node_list)
            i = 0
            num+=1
        elif length <= 20000:
            num += 1
            outfile = 'pruned/tree33_' + str(num) + '.tree'
            st1.write_tree_newick(outfile)
            print('Pruning Complete!')
            prune = False
        else:
            i += 1
filename_df.to_csv('filename_df.tsv', sep = '\t', index = False)
