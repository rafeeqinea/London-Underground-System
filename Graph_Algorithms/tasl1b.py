import random
import time
import matplotlib.pyplot as plt
import math
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

# Network sizes to test
network_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
execution_times = []  # List to store average execution times for each network size

# Generate artificial tube networks and measure execution times
for n in network_sizes:
    # Creating an artificial network with n stations
    graph = AdjacencyListGraph(n, directed=False, weighted=True)

    # Step 1: Adding a spanning tree to ensure connectivity
    for i in range(n - 1):
        travel_time = random.randint(1, 15)
        graph.insert_edge(i, i + 1, travel_time)

    # Step 2: Adding additional random edges to make the graph denser
    num_edges = int(n * 1.5)
    added_edges = set((i, i + 1) for i in range(n - 1))

    while len(added_edges) < num_edges:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if i != j and (i, j) not in added_edges and (j, i) not in added_edges:
            travel_time = random.randint(1, 15)
            graph.insert_edge(i, j, travel_time)
            added_edges.add((i, j))

    # Measuring time for Dijkstra's algorithm, averaged over 10 trials
    trials = []
    for _ in range(10):
        start_node = random.randint(0, n - 1)
        start_time = time.time()
        dijkstra(graph, start_node)
        end_time = time.time()
        trials.append((end_time - start_time) * 1000)  # Converting to milliseconds

    # Calculating and storing the average execution time for this network size
    avg_execution_time = sum(trials) / len(trials)
    execution_times.append(avg_execution_time)
    print(f"Network size: {n}, Average execution time: {avg_execution_time:.4f} milliseconds")

# Ploting empirical vs theoretical time complexities
# Calculating theoretical O(n log n) times and scale them for better visualization
theoretical_times = [n * math.log2(n) for n in network_sizes]  # O(n log n) complexity
scaling_factor = max(execution_times) / max(theoretical_times)  # Scaling to match empirical data
scaled_theoretical_times = [t * scaling_factor for t in theoretical_times]

# Plotting empirical vs theoretical time complexities
plt.figure(figsize=(10, 6))
plt.plot(network_sizes, execution_times, 'bo-', label='Empirical Times')
plt.plot(network_sizes, scaled_theoretical_times, 'r--', label='Theoretical O(n log n)')
plt.xlabel('Network Size (n)')
plt.ylabel('Execution Time (milliseconds)')
plt.title('Empirical vs. Theoretical Time Complexity (Minutes)')
plt.legend()
plt.grid(True)
plt.show()
