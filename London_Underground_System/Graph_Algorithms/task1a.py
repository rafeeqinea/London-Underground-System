from adjacency_list_graph import AdjacencyListGraph  # Imports graph class
from dijkstra import dijkstra                        # Imports Dijkstra's algorithm
from print_path import print_path                    # Imports path printing function

# Defines a small network of tube stations with connections (edges) and travel times (in minutes)
vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']  # List of stations
edges = [
    ('A', 'B', 4), ('A', 'C', 2), ('B', 'D', 5), ('B', 'E', 12),
    ('C', 'D', 2), ('C', 'F', 10), ('D', 'G', 6), ('D', 'E', 3),
    ('E', 'H', 4), ('F', 'G', 3), ('G', 'H', 1), ('H', 'I', 2),
    ('I', 'J', 3)
]

def create_tube_network():
    """
    Creates a graph representation of the tube network with the given stations and edges.
    
    Returns:
        graph: AdjacencyListGraph representing the tube network.
        vertices: List of station names.    
    """
    # Creates an undirected weighted graph
    graph = AdjacencyListGraph(len(vertices), directed=False, weighted=True)
    
    # Adds edges to the graph (each edge has a duration in minutes)
    for edge in edges:
        start_idx = vertices.index(edge[0])  # Finds index of start station
        end_idx = vertices.index(edge[1])    # Finds index of end station
        duration = edge[2]                   # Travels time in minutes
        graph.insert_edge(start_idx, end_idx, duration)  # Adds edge to graph
    
    return graph, vertices

def find_shortest_path(start_station, end_station):
    """
    Finds the shortest path (in terms of travel time) between two stations.
    
    Parameters:
        start_station (str): Name of the starting station.
        end_station (str): Name of the destination station.
    
    Returns:
        dict: Contains the shortest path as a list of station names and the total duration in minutes.
    """
    # Sets up the tube network as a graph
    graph, vertices = create_tube_network()
    
    # Converts station names to their corresponding indices in the graph
    start_idx = vertices.index(start_station)
    end_idx = vertices.index(end_station)
    
    # Uses Dijkstra's algorithm to find shortest path distances and predecessors
    distances, predecessors = dijkstra(graph, start_idx)
    
    # Extract's the shortest path from the start to the end station
    path = print_path(predecessors, start_idx, end_idx, lambda x: vertices[x])
    
    # Return's the path and the total travel time from start to end
    return {
        'path': path,
        'total_duration': distances[end_idx]
    }

# Tests the function with example routes
print("Testing shortest paths in the tube network:")

# Example 1: Find shortest path from A to J
result = find_shortest_path('A', 'J')
print("\nShortest path from A to J:")
print("Path:", ' -> '.join(result['path']))
print("Total travel time:", result['total_duration'], "minutes")

# Example 2: Find shortest path from A to E
result = find_shortest_path('A', 'E')
print("\nShortest path from A to E:")
print("Path:", ' -> '.join(result['path']))
print("Total travel time:", result['total_duration'], "minutes")
