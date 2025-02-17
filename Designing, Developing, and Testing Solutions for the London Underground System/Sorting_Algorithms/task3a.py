import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

# Reading the Excel file
df = pd.read_excel(r'C:\advance ads cw\London Underground data.xlsx', header=None)
df.columns = ['Line', 'From', 'To', 'Time']

# Geting the list of all stations
stations = sorted(list(set(df['From'].dropna().unique()) | set(df['To'].dropna().unique())))
print(f"Found {len(stations)} stations")

# Creating graph
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

# Adding connections between stations
added = set()  # keep track of what we've added
for _, row in df.iterrows():
    if pd.notna(row['To']) and pd.notna(row['Time']):
        start = stations.index(row['From'])
        end = stations.index(row['To'])
        time = row['Time']
                
        edge = tuple(sorted([start, end]))
        if edge not in added:
            graph.insert_edge(start, end, time)
            added.add(edge)

# Finding all possible journeys
journey_times = []
longest = {'time': 0, 'start': None, 'end': None, 'path': None}

for i in range(len(stations)):
    distances, predecessors = dijkstra(graph, i)
    for j in range(i+1, len(stations)):
        if distances[j] != float('inf'):
            journey_times.append(distances[j])
            
            # Checking if this is the longest journey
            if distances[j] > longest['time']:
                path = print_path(predecessors, i, j, lambda x: stations[x])
                longest = {
                    'time': distances[j],
                    'start': stations[i],       
                    'end': stations[j],
                    'path': path
                }

# Making histogram
plt.figure(figsize=(10, 6))
plt.hist(journey_times, bins=110, color='skyblue', edgecolor='black')
plt.xlabel('Journey Time (minutes)')
plt.ylabel('Number of Journeys')
plt.title('How Long Different Journeys Take')
plt.grid(True)
plt.show()

# Printing out what we found
print(f"\nTotal journeys looked at: {len(journey_times)}")
print("\nLongest Journey:")
print(f"Takes {longest['time']} minutes")
print(f"From: {longest['start']}")
print(f"To: {longest['end']}")
print(f"Route: {' -> '.join(longest['path'])}")