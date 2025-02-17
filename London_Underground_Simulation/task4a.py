import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal  # Using library's MST code

# Reading the Excel file
df = pd.read_excel(r'C:\advance ads cw\London Underground data.xlsx', header=None)
df.columns = ['Line', 'From', 'To', 'Time']

# Getting list of stations
stations = sorted(list(set(df['From'].dropna().unique()) | set(df['To'].dropna().unique())))
print(f"Found {len(stations)} stations")

# Creating graph
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

# Adding all connections

added = set()
all_connections = []  # store all connections to check later
for _, row in df.iterrows():
    if pd.notna(row['To']) and pd.notna(row['Time']):
        start = stations.index(row['From'])
        end = stations.index(row['To'])
        time = row['Time']
        
        # Only add if not added before
        edge = tuple(sorted([start, end]))
        if edge not in added:
            graph.insert_edge(start, end, time)
            added.add(edge)
            all_connections.append((row['From'], row['To']))

# Finding minimum spanning tree using library code
mst = kruskal(graph)

# Checking which lines can be closed
closeable_lines = []
for start, end in all_connections:
    start_idx = stations.index(start)
    end_idx = stations.index(end)
    
    # If connection not in MST, it can be closed
    if not mst.has_edge(start_idx, end_idx):
        closeable_lines.append(f"{start} -- {end}")

# Printing out the  results
print(f"\nFound {len(closeable_lines)} line sections that can be closed:")
for line in closeable_lines:
    print(line)