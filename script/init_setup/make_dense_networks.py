from pecanpy import graph
import os

network_lst = os.popen("cat ../../data/networks.txt").read().split()
weighted_lst = os.popen("cat ../../data/weighted.txt").read().split()
weighted_dict = {i:j=='true' for i,j in zip(network_lst, weighted_lst)}

for fp in os.popen("ls ../../data/networks/*.edg").read().split():
    network = os.path.splitext(os.path.split(fp)[1])[0]
    if network == 'SSN200':
        print("Unable to densify SSN200 due to its size")
        continue
    print(f"Start converting: {network}")
    
    g = graph.DenseGraph()
    g.read_edg(fp, weighted=weighted_dict[network], directed=False)
    g.save(f"../../data/networks/dense/{network}.npz")
