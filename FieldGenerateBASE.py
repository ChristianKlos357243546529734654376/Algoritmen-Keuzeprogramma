import networkx as nx
import matplotlib.pyplot as plt
import random
import math

Range = int(input("How big do you want your field? \n"))
Frequency = int(input("How many nodes do you want in your field? \n"))
Connectivity = int(input("How connected do you want your field to be (recommended: 2) \n"))
try:
    MaxRoadLength = int(input(f"What do you want the max length of the edges between nodes to be? \n (press enter without filling anything in to get the recommended value: {Range}) \n"))
except:
    MaxRoadLength = Range
    print(f"Max length between edges set to {MaxRoadLength}")
    
def RandNumber():
    return random.randint(-Range, Range)

def distance(pos1, pos2):
    return float(math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2))

nodes = range(1, Frequency+1)
G = nx.Graph()
G.add_nodes_from(['C', 'NW', 'NE', 'SE', 'SW'] + list(nodes))

pos = {
    'C': (0, 0),
    'NW': (-(Range+5), (Range+5)),
    'NE': ((Range+5), (Range+5)),
    'SE': ((Range+5), -(Range+5)),
    'SW': (-(Range+5), -(Range+5)),
}
pos.update({node: (RandNumber(), RandNumber()) for node in nodes})

def add_edges_to_closest():
    for node in nodes:
        minDist = math.inf
        closestNode = None

        for otherNode in nodes:
            if node != otherNode and not G.has_edge(node, otherNode):
                dist = distance(pos[node], pos[otherNode])
                if dist < minDist and dist < MaxRoadLength:
                    minDist = dist
                    closestNode = otherNode

        if closestNode is not None:
            G.add_edge(node, closestNode)
            print(f"Added edge between node {node:<2} and node {closestNode:<2} with a distance of about {round(distance(pos[node], pos[closestNode]), 2):<8}")

for i in range(Connectivity):
    add_edges_to_closest()

nx.draw(G, pos, with_labels=True, node_color='white', edge_color='gray', node_size=100, font_color='black', font_size=7)
plt.show()
