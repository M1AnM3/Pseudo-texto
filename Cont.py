import networkx as nx
import math
import random
import re
import numpy as np

def calculate_positions(G, Narb, N1, N2):
    positions = {}
    num_nodes = len(G.nodes)
    for i, node in enumerate(G.nodes):
        if node in Narb:
            positions[node] = (i,1)
        elif node in N1:
            positions[node] = (i,0)
        elif node in N2:
            positions[node] = (i,-1)
    return positions

def split_sentence(sentence):
    return [word for word in re.findall(r'\b\w+\b|[^\w\s]', sentence)] #'\b\w+\b|[^\w\s]|\s' #'\b\w+\b|[^a-zA-Z0-9\s]'

def DiGraphCo(A):
  Aa = [sentence.split(' ') for sentence in A] #[split_sentence(A[i]) for i in range(len(A))]

  G = nx.DiGraph()

  for i in range(len(A)):
      for j in range(len(Aa[i])-1):
          G.add_edge(Aa[i][j],Aa[i][j+1])

  return G

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

def RedDigraph(G):
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

  return H

def SigNodo(list_of_current_node, current_node, quasi_kernel, graph):
    if current_node in quasi_kernel:
        neighbors = [neighbor for neighbor in graph[current_node] if neighbor not in quasi_kernel and set(current_node)]
        if neighbors:
            return random.choice(neighbors)
    elif current_node in N1:
        neighbors = [neighbor for neighbor in graph[current_node] if neighbor in quasi_kernel]
        if neighbors:
            return random.choice(neighbors)
    elif current_node in N2:
        neighbors = [neighbor for neighbor in graph[current_node] if neighbor in N1]
        if neighbors:
            return random.choice(neighbors)
    return None

A = [
    "Un gato ve un gato",
    "Hola, como estas?",
    "Quien soy?",
    "Como entrenar un programa?",
    "Agua en la tierra."
] #Este es un ejemplo muy simple


############################################################################
# Para "platicar"
############################################################################

print("Escriba 'salir' para acabar el programa.")

while True:
    texto_input = input("User: ")

    if texto_input.lower() == 'salir':
        print("Cerrando el programa")
        break

    B = [texto_input]

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    #
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    A.append(B[0])

    G = DiGraphCo(A)

    nodes = list(G.nodes())

    Po = [node for node in nodes if G.out_degree(node)==0]

    ####################################################################################################################
    #Reduciendo la digráfica original
    ####################################################################################################################

    NodesToElim = []

    H = RedDigraph(G)

    H_nodes = list(H.nodes())

    ####################################################################################################################
    # Completando el quasi-núcleo de H a uno de G
    ####################################################################################################################

    Narb = set()

    if nx.is_weakly_connected(H):
      Narb = refine_set(H)
    else:
      for C in nx.weakly_connected_components(H):
        Narb.update(refine_set(H.subgraph(list(C))))

    ####################################################################################################################
    # Completando el quasi-núcleo de H a uno de G
    ####################################################################################################################

    Inv_Original_NodesToElim = list(reversed(NodesToElim))

    for n in range(0,len(NodesToElim)):

        Narb_copy = Narb.copy()

        if any(G.has_edge(Inv_Original_NodesToElim[n],s) or G.has_edge(s,Inv_Original_NodesToElim[n]) for s in Narb_copy):
            continue
        else:
            Narb.add(Inv_Original_NodesToElim[n])

    ####################################################################################################################
    # Info básica de la digráfica y casi-núcleo
    ####################################################################################################################

    N1 = set(v for v in set(G.nodes-Narb) if any(nx.shortest_path_length(G, v, s) == 1 for s in Narb if nx.has_path(G, v, s)))

    N2 = set(v for v in set(G.nodes-Narb-N1) if any(nx.shortest_path_length(G, v, s) == 2 for s in Narb if nx.has_path(G, v, s)))

    pos = calculate_positions(G, Narb, N1, N2)

    file_path = "elements.txt"

    with open(file_path, 'w') as file:
        for element in list(Narb):
            file.write(element + "\n")

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    #
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    Bb = B[0].split(' ') #split_sentence(B[0])

    InCam = Bb[-1]
    path = Bb

    Continuator = [B[0]]
    
    for _ in range(100):
        next_node = SigNodo(Bb, InCam, Narb, G)
        if next_node is None:
            break
        elif "." == next_node or "?" in next_node or "!" in next_node: #next_node is None:
            Continuator.append(next_node)
            InCam = next_node
            break

        Continuator.append(next_node)
        InCam = next_node

    if len(Continuator) == 0:
      print('Continuator : Perdón no se como responder.')
    else:
      print(f'Continuator: {" ".join(Continuator)}')
