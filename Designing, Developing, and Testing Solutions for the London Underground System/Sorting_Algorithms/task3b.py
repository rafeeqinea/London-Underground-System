import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

# Reading the Excel file 
print("Reading tube data...")
df = pd.read_excel(r'C:\advance ads cw\London Underground data.xlsx', header=None)
df.columns = ['Line', 'From', 'To', 'Time']

# Getting the list of all stations
stations = sorted(list(set(df['From'].dropna().unique()) | set(df['To'].dropna().unique())))
print(f"Found {len(stations)} stations")

# Creating graph
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

# Adding connections between stations (weight=1 for each stop)
added = set()
for _, row in df.iterrows():
   if pd.notna(row['To']):  # just need To station, don't need Time
       start = stations.index(row['From'])
       end = stations.index(row['To'])
       
       # adding if we haven't added it yet
       edge = tuple(sorted([start, end]))
       if edge not in added:
           graph.insert_edge(start, end, 1)  # weight=1 means one stop
           added.add(edge)

# Finding all possible journeys
journey_stops = []
longest = {'stops': 0, 'start': None, 'end': None, 'path': None}

for i in range(len(stations)):
   distances, predecessors = dijkstra(graph, i)
   for j in range(i+1, len(stations)):
       if distances[j] != float('inf'):
           journey_stops.append(distances[j])
           
           # Checking if this has most stops
           if distances[j] > longest['stops']:
               path = print_path(predecessors, i, j, lambda x: stations[x])
               longest = {
                   'stops': distances[j],
                   'start': stations[i],
                   'end': stations[j],
                   'path': path
               }

# Making histogram
plt.figure(figsize=(10, 6))
plt.hist(journey_stops, bins=38, color='lightgreen', edgecolor='black')
plt.xlabel('Number of Stops')
plt.ylabel('Number of Journeys')
plt.title('How Many Stops Different Journeys Take')
plt.grid(True)
plt.show()

# Printing what we found
print(f"\nTotal journeys looked at: {len(journey_stops)}")
print("\nJourney with Most Stops:")
print(f"Takes {longest['stops']} stops")
print(f"From: {longest['start']}")
print(f"To: {longest['end']}")
print(f"Route: {' -> '.join(longest['path'])}")