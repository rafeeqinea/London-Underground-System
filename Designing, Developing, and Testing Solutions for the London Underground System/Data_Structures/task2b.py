import random
import time
import matplotlib.pyplot as plt
import numpy as np
import math
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

# Defined network sizes to test (increased sizes for Task 2b)
network_sizes = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
execution_times = []  # List's to store average execution times for each network size

# Measuring execution time for each network size using Dijkstra's algorithm
for n in network_sizes:
    # Createing a graph with `n` stations and a higher number of random connections to ensure connectivity
    graph = AdjacencyListGraph(n, directed=False, weighted=True)
    
    # Step 1: Ensuring the graph is connected by adding a spanning tree (all edges weight = 1)
    for i in range(n - 1):
        graph.insert_edge(i, i + 1, 1)  # Edge weight set to 1 to represent a single stop
    
    # Step 2: Adding additional random edges to make the graph denser
    num_edges = int(n * 2.5)  # Increasing edge count for a denser graph
    added_edges = set((i, i + 1) for i in range(n - 1))  # Tracking the edges that were added in spanning tree
    
    while len(added_edges) < num_edges:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if i != j and (i, j) not in added_edges and (j, i) not in added_edges:
            graph.insert_edge(i, j, 1)  # Edge weight set to 1 for uniform stop count
            added_edges.add((i, j))

    # Measuring time for Dijkstra's algorithm, averaged over 10 trials
    trials = []
    for _ in range(10):
        start = random.randint(0, n - 1)
        start_time = time.time()
        dijkstra(graph, start)
        end_time = time.time()
        trials.append((end_time - start_time) * 1000)  # Converting to milliseconds
    
    # Calculating and storing the average execution time for this network size
    avg_time = sum(trials) / len(trials)
    execution_times.append(avg_time)
    print(f"Network size: {n}, Average execution time: {avg_time:.4f} milliseconds")

# Calculating theoretical O(n log n) times and scales them for better visualization
theoretical_times = [n * math.log2(n) for n in network_sizes]  # O(n log n) complexity
scaling_factor = max(execution_times) / max(theoretical_times)  # Scaling to match empirical data
scaled_theoretical_times = [t * scaling_factor for t in theoretical_times]

# Plotting empirical vs theoretical time complexities
plt.figure(figsize=(10, 6))
plt.plot(network_sizes, execution_times, 'bo-', label='Empirical Times (Dijkstra)')
plt.plot(network_sizes, scaled_theoretical_times, 'r--', label='Theoretical O(n log n)')
plt.xlabel('Network Size (n)')
plt.ylabel('Execution Time (milliseconds)')
plt.title('Empirical vs. Theoretical Time Complexity (Stops)')
plt.legend()
plt.grid(True)
plt.show()
