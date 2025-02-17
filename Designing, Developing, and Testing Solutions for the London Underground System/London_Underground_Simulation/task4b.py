import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path
from mst import kruskal  # Need this to find closeable lines

# Reading the Excel file
df = pd.read_excel(r'C:\advance ads cw\London Underground data.xlsx', header=None)
df.columns = ['Line', 'From', 'To', 'Time']

# Getting out the stations
stations = sorted(list(set(df['From'].dropna().unique()) | set(df['To'].dropna().unique())))
print(f"Found {len(stations)} stations")

# First get original graph and MST
original = AdjacencyListGraph(len(stations), directed=False, weighted=True)
added = set()

# Adding connections to original graph
for _, row in df.iterrows():
    if pd.notna(row['To']) and pd.notna(row['Time']):
        start = stations.index(row['From'])
        end = stations.index(row['To'])
        time = row['Time']
        
        edge = tuple(sorted([start, end]))
        if edge not in added:
            original.insert_edge(start, end, time)
            added.add(edge)

# Getting MST for reduced network
reduced = kruskal(original)

# Finding out all journey times for both networks
original_times = []
longest_original = {'time': 0, 'path': None, 'start': None, 'end': None}

for i in range(len(stations)):
    distances, predecessors = dijkstra(original, i)
    for j in range(i+1, len(stations)):
        if distances[j] != float('inf'):
            original_times.append(distances[j])
            
            if distances[j] > longest_original['time']:
                path = print_path(predecessors, i, j, lambda x: stations[x])
                longest_original = {
                    'time': distances[j],
                    'start': stations[i],
                    'end': stations[j],
                    'path': path
                }

reduced_times = []
longest_reduced = {'time': 0, 'path': None, 'start': None, 'end': None}

for i in range(len(stations)):
    distances, predecessors = dijkstra(reduced, i)
    for j in range(i+1, len(stations)):
        if distances[j] != float('inf'):
            reduced_times.append(distances[j])
            
            if distances[j] > longest_reduced['time']:
                path = print_path(predecessors, i, j, lambda x: stations[x])
                longest_reduced = {
                    'time': distances[j],
                    'start': stations[i],
                    'end': stations[j],
                    'path': path
                }

# Creating side-by-side histograms
plt.figure(figsize=(12, 5))

# Original network
plt.subplot(1, 2, 1)
plt.hist(original_times, bins=110, color='skyblue', edgecolor='black')
plt.xlabel('Journey Time (minutes)')
plt.ylabel('Number of Routes')
plt.title('Before Closures')
plt.grid(True)

# Reduced network
plt.subplot(1, 2, 2)
plt.hist(reduced_times, bins=120, color='lightcoral', edgecolor='black')
plt.xlabel('Journey Time (minutes)')
plt.ylabel('Number of Routes')
plt.title('After Closures')
plt.grid(True)

plt.tight_layout()
plt.show()

# Printing comparison
print("\nComparison:")
print(f"Original network: {len(original_times)} possible journeys")
print(f"Reduced network: {len(reduced_times)} possible journeys")
print(f"\nLongest journey before closures:")
print(f"Time: {longest_original['time']} minutes")
print(f"From: {longest_original['start']}")
print(f"To: {longest_original['end']}")
print(f"Route: {' -> '.join(longest_original['path'])}")
print(f"\nLongest journey after closures:")
print(f"Time: {longest_reduced['time']} minutes")
print(f"From: {longest_reduced['start']}")
print(f"To: {longest_reduced['end']}")
print(f"Route: {' -> '.join(longest_reduced['path'])}")


