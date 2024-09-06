import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import StandardScaler
import os
from collections import Counter, deque, defaultdict
import networkx as nx

def cluster_and_plot(folder_path, num_clusters, method = 'kMeans'):
    
    # file path
    TFname_file = os.path.join(folder_path, 'TFName.txt')
    TGname_file = os.path.join(folder_path, 'TGName.txt')
    score_file = os.path.join(folder_path, 'TFTG_regulationScore.txt')
    
    TFnames = pd.read_csv(TFname_file, header=None).squeeze().tolist()
    TGnames = pd.read_csv(TGname_file, header=None).squeeze().tolist()

    # score
    scores = np.loadtxt(score_file)
    scores[scores < 0] = 0
    scores[np.isnan(scores)] = 0
    scores_normalized = np.log(scores + 1)

    if method == 'KMeans':
        # TF cluster
        kmeans_TF = KMeans(n_clusters=num_clusters, random_state=0)
        TF_labels = kmeans_TF.fit_predict(scores_normalized)

        # TG cluster
        kmeans_TG = KMeans(n_clusters=num_clusters, random_state=0)
        TG_labels = kmeans_TG.fit_predict(scores_normalized.T)

    elif method == 'Spectral':
        spectral_TF = SpectralClustering(n_clusters=3, affinity='nearest_neighbors', random_state=0)
        TF_labels = spectral_TF.fit_predict(scores_normalized)

        spectral_TG = SpectralClustering(n_clusters=3, affinity='nearest_neighbors', random_state=0)
        TG_labels = spectral_TG.fit_predict(scores_normalized.T)    
    
    else:
        print('Unrecognized clustering methods, please input KMeans or Spectral!')

    
    sorted_TF_indices = np.argsort(TF_labels)
    sorted_TG_indices = np.argsort(TG_labels)

    # sorted_TF_names = np.take(TFnames, sorted_TF_indices)
    # sorted_TG_names = np.take(TGnames, sorted_TG_indices)
    sorted_scores = scores_normalized[sorted_TF_indices][:, sorted_TG_indices]

    modules = {i: {'TFs': [], 'TGs': []} for i in range(num_clusters)}

    for i in range(len(TF_labels)):
        cluster_id = TF_labels[i]
        modules[cluster_id]['TFs'].append(TFnames[i])
    
    for j in range(len(TG_labels)):
        cluster_id = TG_labels[j]
        modules[cluster_id]['TGs'].append(TGnames[j])

    with open(os.path.join(folder_path, 'TFmodule_results.txt'), 'w') as f:
        for cluster_id, names in modules.items():
            f.write(f"Module {cluster_id + 1}:\n")
            f.write("TFs: " + ", ".join(names['TFs']) + "\n")

    with open(os.path.join(folder_path, 'TGmodule_results.txt'), 'w') as f:
        for cluster_id, names in modules.items():
            f.write(f"Module {cluster_id + 1}:\n")
            f.write("TGs: " + ", ".join(names['TGs']) + "\n")

    # heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(sorted_scores, aspect='auto', cmap='viridis')
    plt.colorbar()

    plt.savefig(os.path.join(folder_path, 'co_module.png'), format='png')

def _tf_layer(folder_path, output_file='TF_layer.txt'):
    
    TFname_file = os.path.join(folder_path, 'TFName.txt')
    TGname_file = os.path.join(folder_path, 'TGName.txt')
    score_file = os.path.join(folder_path, 'TFTG_regulationScore.txt')

    TFnames = pd.read_csv(TFname_file, header=None).squeeze().tolist()
    TGnames = pd.read_csv(TGname_file, header=None).squeeze().tolist()

    scores = np.loadtxt(score_file)
    scores[scores < 0] = 0
    scores[np.isnan(scores)] = 0
    scores_normalized = np.log(scores + 1)

    network_file = None
    for file in os.listdir(folder_path):
        if file.endswith('network.txt'):
            network_file = os.path.join(folder_path, file)
            break
    net = pd.read_csv(network_file, sep='\t')
    net = net.iloc[:,0:2]

    TF_net = net[net['TF'].isin(TFnames) & net['TG'].isin(TFnames)]

    # Graph
    G = nx.DiGraph()
    for _, row in TF_net.iterrows():
        G.add_edge(row['TF'], row['TG'])
    
    initial_tfs = set(TF_net['TF']) - set(TF_net['TG'])

    # BFS
    layers = {}
    visited = set()
    queue = [(0, tf) for tf in initial_tfs]  # (layer, TF)
    
    while queue:
        layer, current_tf = queue.pop(0)
        if current_tf not in visited:
            visited.add(current_tf)
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(current_tf)
            neighbors = G.successors(current_tf)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((layer + 1, neighbor))
    
    with open(os.path.join(folder_path,output_file), 'w') as f:
        for layer in sorted(layers.keys()):
            f.write(f"Layer {layer}: {', '.join(layers[layer])}\n")

def _top_tf_layer_plot(folder_path, graph_file='top_TF_layer_graph.png'):
    TFname_file = os.path.join(folder_path, 'TFName.txt')
    TGname_file = os.path.join(folder_path, 'TGName.txt')
    score_file = os.path.join(folder_path, 'TFTG_regulationScore.txt')

    TFnames = pd.read_csv(TFname_file, header=None).squeeze().tolist()
    TGnames = pd.read_csv(TGname_file, header=None).squeeze().tolist()

    scores = np.loadtxt(score_file)
    scores[scores < 0] = 0
    scores[np.isnan(scores)] = 0
    scores_normalized = np.log(scores + 1)

    network_file = None
    for file in os.listdir(folder_path):
        if file.endswith('network.txt'):
            network_file = os.path.join(folder_path, file)
            break
    net = pd.read_csv(network_file, sep='\t')
    net = net.iloc[:,0:2]

    TF_score = np.sum(scores_normalized, axis=1)
    sorted_indices = np.argsort(TF_score)[::-1]
    num_tfs = max(int(len(TFnames)*0.2), 50)
    top_tf_indices = sorted_indices[:num_tfs]
    top_TF = [TFnames[i] for i in top_tf_indices]
    TF_net = net[net['TF'].isin(top_TF) & net['TG'].isin(top_TF)]
    initial_tfs = set(TF_net['TF']) - set(TF_net['TG'])
    G = nx.DiGraph()
    for _, row in TF_net.iterrows():
        G.add_edge(row['TF'], row['TG'])
    
    layers = {}
    visited = set()
    queue = [(0, tf) for tf in initial_tfs] 
        
    while queue:
        layer, current_tf = queue.pop(0)
        if current_tf not in visited:
            visited.add(current_tf)
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(current_tf)
            neighbors = G.successors(current_tf)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((layer + 1, neighbor))

    pos = {}
    layer_y = -len(layers) / 2  # position
    for layer in sorted(layers.keys()):
        nodes = layers[layer]
        layer_x = (len(nodes) - 1) / 2  
        for i, node in enumerate(nodes):
            pos[node] = (i, layer_y)
        layer_y += 1  

    fig, ax = plt.subplots()
    nx.draw(G, pos, ax=ax,with_labels=False, arrows=True, node_size=20, edge_color='orange')

    for node in G.nodes():
        x, y = pos[node]  
        plt.text(x, y + 0.1, str(node), fontsize=12, ha='center', va='bottom', rotation=90)

    plt.title("topTF Layer Graph")
    plt.savefig(os.path.join(folder_path,graph_file))
    plt.close()