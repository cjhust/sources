# -*- coding: utf-8 -*-
#!/usr/local/bin/python


import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


G=nx.Graph()
G.add_node(1)
G.add_nodes_from([2,3,4,5,6,7,8,9,10])
nx.draw(G)
plt.savefig("first.png")

