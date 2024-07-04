import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
import math
import random
import re
import numpy as np

####################################################################################################################
#Extracción de palabras y caracteres especiales para formar una digráfica de co-ocurrencia
####################################################################################################################

A = ["Un texto de ejemplo", "Varios textos de ejemplo", "Un gato ve un gato", "Un día, camine y encontre un gato"]

def split_sentence(sentence):
    return [word for word in re.findall(r'\b\w+\b|[^\w\s]', sentence)]

Aa = [split_sentence(A[i]) for i in range(len(A))]

G = nx.DiGraph()

for i in range(len(A)):
    for j in range(len(Aa[i])-1):
        G.add_edge(Aa[i][j],Aa[i][j+1])

nodes = list(G.nodes())

Po = [node for node in nodes if G.out_degree(node)==0]

####################################################################################################################
#Reduciendo la digráfica original
####################################################################################################################

NodesToElim = []

Rev_nodes = list(reversed(nodes))

H = G.copy()

for n in range(0,len(nodes)-5):
    v = Rev_nodes[n]
    Pred_v = G.predecessors(v)

    H_nodes = list(H.nodes())

    if v in H_nodes:
        NodesToElim.append(v)
        H.remove_node(v)
        H.remove_nodes_from(Pred_v)

H_nodes = list(H.nodes())

####################################################################################################################
# Encontrando el quasi-núcleo de la digráfica reducida
####################################################################################################################

print(nx.is_weakly_connected(H))

def find_max_independent_set(graph):
    mis = set()
    nodes = list(graph.nodes())

    while nodes:
        node = nodes.pop()
        mis.add(node)
        nodes = [n for n in nodes if not (n in graph[node] or node in graph[n])]

    return mis

def dist_2(G, S):
    for node in set(G.nodes) - S:
        if all(nx.shortest_path_length(G, node, s) > 2 for s in S if nx.has_path(G, node, s)):
            return False
    return True

def refine_set(G):
    S = find_max_independent_set(G)
    while not dist_2(G, S):
        S = find_max_independent_set(G)
    return S

Narb = set()

if nx.is_weakly_connected(H):
  Narb = refine_set(H)
else:
  for C in nx.weakly_connected_components(H):

    Narb.update(refine_set(H.subgraph(list(C))))
    print(f'{C}\n {refine_set(H.subgraph(list(C)))}')

print(f'Quasi-núcleo de la digráfica reducida: {Narb}\n')

####################################################################################################################
# Completando el quasi-núcleo de la digráfica reducida a una de la original
###################################################################################################################

Inv_Original_NodesToElim = list(reversed(NodesToElim))

for n in range(0,len(NodesToElim)):

    Narb_copy = Narb.copy()

    if any(G.has_edge(Inv_Original_NodesToElim[n],s) or G.has_edge(s,Inv_Original_NodesToElim[n]) for s in Narb_copy):
        continue 
    else:
        Narb.add(Inv_Original_NodesToElim[n])

if any(G.has_edge(u,v) for u in Narb for v in Narb):
    print('Hay lazos')

####################################################################################################################
# Info básica de la digráfica y casi-núcleo
####################################################################################################################

N1 = set(v for v in set(G.nodes-Narb) if any(nx.shortest_path_length(G, v, s) == 1 for s in Narb if nx.has_path(G, v, s)))

N2 = set(v for v in set(G.nodes-Narb-N1) if any(nx.shortest_path_length(G, v, s) == 2 for s in Narb if nx.has_path(G, v, s)))

print(f"""Palabras:{Aa}\n
    Cantidad de palabras: {len(G.nodes)}\n
    Cantidad de textos: {len(A)}\n
    Flechas en la digráfica: {G.edges.data()}\n
    Nodos de la digráfica reducida:{H_nodes}\n
    Flechas en la digráfica reducida: {H.edges.data()}\n
    Quasi-Núcleo de la digráfica original: {Narb}\n
    Cardinalidad del quasi-núcleo: {len(Narb)}\n
    No quasi-núcleo: {set(G.nodes - Narb)}\n
    Nodos1: {N1}\n
    Cant.Nodos1: {len(N1)}\n
    Nodos2: {N2}\n
    Cant.Nodos2: {len(N2)}\n
    Pozos de la digráfica original: {Po}""")

####################################################################################################################
#Generando pseudo-oraciones
####################################################################################################################

def SigNodo(current_node, quasi_kernel, graph):
    if current_node in quasi_kernel:
        for neighbor in graph[current_node]:
            if neighbor not in quasi_kernel:
                return neighbor
    elif current_node in N1:
        for neighbor in graph[current_node]:
            if neighbor in quasi_kernel:
                return neighbor
    elif current_node in N2:
        for neighbor in graph[current_node]:
            if neighbor in N1:
                return neighbor
    return None

nodeso = list(G.nodes())

for m in range(50):
  InCam = random.choice(nodeso)
  path = [InCam]
  for _ in range(50):
      next_node = SigNodo(InCam, Narb, G)
      if next_node is None:
          break
      path.append(next_node)
      InCam = next_node

  print(f'Camino dirigido: {" ".join(path)}')

####################################################################################################################
# Función para acomodar los vértices en tres círculos dependiendo de su relación con el quasi-núcleo
####################################################################################################################

def calculate_positions(G, Narb, N1, N2):
    positions = {}
    num_nodes = len(G.nodes)
    for i, node in enumerate(G.nodes):
        if node in Narb:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (3 * math.cos(theta), 3 * math.sin(theta))
        elif node in N1:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (2 * math.cos(theta), 2 * math.sin(theta))
        elif node in N2:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (math.cos(theta), math.sin(theta))
    return positions

############################################################################
# Para vizualizar la digráfica
############################################################################

pos = calculate_positions(G, Narb, N1, N2)

node_colors = ["skyblue" if node in Narb else "red" if node in N1 else "green" for node in G.nodes]
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=40)
nx.draw_networkx_edges(G, pos, arrowsize=10)
plt.axis("off")

crs = mplcursors.cursor(hover=True)

crs.connect("add", lambda sel: sel.annotation.set_text(f'{list(G.nodes)[sel.target.index]} (in-grado: {G.in_degree(list(G.nodes)[sel.target.index])})'))

plt.show()
