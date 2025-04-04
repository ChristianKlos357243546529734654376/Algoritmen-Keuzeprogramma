#Grafiek en Grafiek functionaliteiten geleert van de NetworkX officiele website:
#https://networkx.org/documentation/stable/tutorial.html
import networkx as nx

#Heel veel uitleg gebruikt van de matplotlib officiele website:
#https://matplotlib.org/stable/users/index.html
import matplotlib.pyplot as plt

#Standaard Python Libraries
import random
import math
import threading
import time

#4 verschillende try excepts voor de zekerheid
try:
    Range = int(input("How big do you want your field? (Recommended 25) \n"))
except:
    Range = 25
    print(f"Error: Max length between edges set to {Range} \n")

try:
    Frequency = int(input("How many nodes do you want in your field? (Recommended 10) \n"))
except:
    Frequency = 10
    print(f"Error: Max length between edges set to {Frequency} \n")

try:
    Connectivity = int(input("How connected do you want your field to be (Recommended 2) \n"))
except:
    Connectivity = 2
    print(f"Error: Max length between edges set to {Connectivity} \n")

try:
    MaxRoadLength = int(input(f"What do you want the max length of the edges between nodes to be? (Recommended {Range}) \n"))
except:
    MaxRoadLength = Range
    print(f"Error: Max length between edges set to {MaxRoadLength} \n")
    
#Genereert gerandomiseerde coördinaten, om de nodes op willekeurige plekken op de grafiek te plotten
def RandNumber():
    return random.randint(-Range, Range)

#Gebruikt pythagoras om de afstand tussen twee punten op de grafiek te vinden, inmiddels heb ik uitgevonden dat matplotlib hier automatisch iets voor heeft, maar deze heb ik inmiddels zoveel gebruikt dat ik deze ga houden
def distance(pos1, pos2):
    return float(math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2))

#Creëert nodes gelijk aan de hoeveelheid die is ingevult bij 'frequency', begint bij 1 en telt op
nodes = range(1, Frequency+1)
#Creëert Grafiek en voegtnodes toe
G = nx.Graph()
G.add_nodes_from(['NW', 'NE', 'SE', 'SW'] + list(nodes))

#Creëert een dictionary van 4 Coördinaten gelijk aan de range +5 (zodat ze net buiten de range zitten), deze waardes zorgen ervoor dat de view window consistent is en altijd alle nodes bevat, verder onbelangrijk.
pos = {
    'NW': (-(Range+5), (Range+5)),
    'NE': ((Range+5), (Range+5)),
    'SE': ((Range+5), -(Range+5)),
    'SW': (-(Range+5), -(Range+5)),
}

#Gebruikt een list comprehended for loop om  willekeurige coördinaten te bedenken voor alle nodes (behalve NW, NE,SE, en SW)
#https://www.w3schools.com/python/python_lists_comprehension.asp
pos.update({node: (RandNumber(), RandNumber()) for node in nodes})

#Deze def kijkt naar  wat de dichtbijzijndste nodes zijn, en creërt daar een lijn tussen, zolang het minder dan de MaxRoadLength is
def addEdgesToClosest():
    for node in nodes:
        #math.inf gebruikt zodat de minDist ALTIJD lager wordt als het veranderd word (math.inf is oneindig)
        #https://docs.python.org/3/library/math.html
        minDist = math.inf
        #Stelt de ClosestNode als None zodat er geen errors optreden
        closestNode = None

        for otherNode in nodes:
            #Voert de code niet uit als de twee edges hetzelfde zijn, of als ze al een edge hebben
            if node != otherNode and not G.has_edge(node, otherNode):
                #Berekent afstand tussen de twee nodes, zodat het te vergelijken met minDist en MaxRoadLength is
                dist = distance(pos[node], pos[otherNode])
                if dist < minDist and dist < MaxRoadLength:
                    minDist = dist
                    closestNode = otherNode

        if closestNode is not None:
            G.add_edge(node, closestNode)
            #Veel formatting gebruikt van w3schools voor de leesbaarheid, specefiek de :<3, wat bijna functioneert als tab in de print
            #https://www.w3schools.com/python/python_string_formatting.asp
            print(f"Added edge between node {node:<3} and node {closestNode:<3} with a distance of about {round(distance(pos[node], pos[closestNode]), 2)}")


#Voert de verbindingsproces uit een hoeveelheid keer gelijk aan de 'connectivity' waarde
for i in range(Connectivity):
    addEdgesToClosest()


nx.draw(G, pos, with_labels=True, node_color='white', edge_color='gray', node_size=100, font_color='black', font_size=7)
#Threading werkt niet samen met matplotlib, dus moet het helaas maar zo
print("\n \n CLOSE THE PLOT WHEN READY TO CALCULATE")
plt.show()

try:
    StartNode = int(input("What node do you want to be your Starting Point? \n"))
except:
    StartNode = 1
    print(f"Error, Destination Node set to {StartNode}")

try:
    DestNode = int(input("What node do you want to be your Destination \n"))
except:
    DestNode = Frequency
    print(f"Error, Destination Node set to {DestNode}")

# Kijkt naar de Dictionary van edges (automatisch gecreert door matplotlib), en verandert de 'weight' variabel in de afstand tussen de twee nodes
for InNode, OutNode in G.edges():
    G[InNode][OutNode]['weight'] = distance(pos[InNode], pos[OutNode])

"""Voor Proces en uitleg over Breadth First Searches (de methode die ik heb gebruikt) heb ik de CS50 Lecture gekeken en gevolgt:
https://www.youtube.com/watch?v=WbzNRTTrX0g&t=2510s"""


def FindRoute(graph, start, goal):
    #TotalDistance begint bij 0.
    TotalDistance = 0
    #Frontier is een lijst die bestaat uit een tupel met een lijst erin, het bevat 3 waardes in de tupel
    #TotalDistance = De afstand die deze 'frontier' heeft gedaan
    #start = De node waar de frontier huidig op zit
    #[start] = Een lijst waar alle nodes waar de specefieke frontier langs is gegaan
    frontiers = [(TotalDistance, start, [start])]
    #Maakt zeker dat we niet twee keer over dezelfde node heen gaan.
    visited = []
    
    #Deze hier zodat we later de totale afstand kunnen gebruiken als 'key' (Om de correcte waarde op te halen bij het sorteren) om de frontier te sorteren
    def getDistance(TotalDistance):
    #Index [0] is TotalDistance in de tupel
        return TotalDistance[0]
    
    while frontiers:
        #Sorteert bij de kortste 'distance', zodat ieder afstand met gelijke snelheid wordt gemeten.
        #https://www.w3schools.com/python/python_tuples.asp
        frontiers.sort(key=getDistance)
        #verwijderd de frontier die de code gaat uitbreiden, maar neemt eerst de waardes voor de calculatie.
        distSoFar, current, path = frontiers.pop(0)

        if current == goal:
            #Returned de path en de TotalDistance zodra de oplossing is gevonden, wat (omdat het telkens de kortste frontier berekent) altijd de kortste route als eerste geeft
            return path, distSoFar

        elif current in visited:
            continue
        
        #voegt de huidige node toe aan visited, zodat we nooit twee keer langs dezelfde node gaan
        visited.append(current)
        
        #Deze for loop kijkt naar alle 'neighbours' (alle nodes die verbonden zijn met een edge), berekent de afstand om ernaar te gaan, en voegt die frontier too aan frontiers
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                edgeWeight = graph[current][neighbor].get('weight')
                #Voegt de nieuwe frontier toe, update de Total Distance, Huidige Node, En voegt de huidige node toe aan de path
                frontiers.append((distSoFar + edgeWeight, neighbor, path + [neighbor]))
                print(frontiers)

try:
    path, TotalDistanceQuickestRoute = FindRoute(G, StartNode, DestNode)
    print(f"Path from node {StartNode} to node {DestNode}: {path} with total distance {round(TotalDistanceQuickestRoute, 2)}")
    # Zipped twee lijsten, eentje van 'path' en eentje van 'path[1:]' (Path maar dan met alle waardes 1 index plek opgeschoven zodat de zip zowel de begin als eindwaarde van de node in een tuple zet)
    # https://www.w3schools.com/python/ref_func_zip.asp
    # https://www.w3schools.com/python/python_lists_access.asp
    # Veranderd de kleuren en dikte van de edges als ze in de path zijn.
    edge_colors = ['red' if (Node1, Node2) in zip(path, path[1:]) or (Node2, Node1) in zip(path, path[1:]) else 'gray' for Node1, Node2 in G.edges()]
    edge_widths = [ 2 if (Node1, Node2) in zip(path, path[1:]) or (Node2, Node1) in zip(path, path[1:]) else 1 for Node1, Node2 in G.edges()]

    # Veranderd de kleuren van de nodes zelf als ze in de path zijn.
    node_colors = ['red' if node in path else 'white' for node in G.nodes()]
    nodeSizes = [75 if node in path else 0 for node in G.nodes()]

    #Chatgpt gebruikt voor deze lijn, dit zorgt erboor dat alleen de nodes in de path een Label krijgen.
    nodeLabels = {node: node for node in path}
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=nodeSizes, font_color='black', font_size=7, edge_color=edge_colors, width=edge_widths, labels=nodeLabels)

    plt.show()
except:
    print(f"No available path from node {StartNode} to node {DestNode}")
