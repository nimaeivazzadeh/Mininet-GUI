#!/usr/bin/env python3

import json
import networkx as nx
import matplotlib.pyplot as plt

filename = './topology.json'

with open(filename, 'r') as infile:
    topology = json.loads(infile.read())

nodes = topology['Switches'] + topology['Hosts']
path = topology['Path']
labels = {}
edges_all = []
edges_path = []
G = nx.DiGraph()

for link in topology['Links']:
    for A, B in link.items():
         A_name = A.split('-')[0]
         A_if = A.split('-')[1]
         B_name = B.split('-')[0]
         B_if = B.split('-')[1]
         edges_all.append([A_name, B_name])
         labels[(A_name, B_name)] = A_if
         labels[(B_name, A_name)] = B_if

for i in range(0, len(path) - 1):
    edges_path.append([path[i], path[i + 1]])

# print(nodes)
# print(edges_all)
# print(edges_path)
# print(labels)

G.add_nodes_from(nodes)
G.add_edges_from(edges_all)

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows = False)
nx.draw_networkx_edges(G, pos, edges_path, edge_color = '#00FF00', arrowsize=20)
nx.draw_networkx_edge_labels(G, pos, labels, 0.2)

plt.axis('off')
plt.show()
