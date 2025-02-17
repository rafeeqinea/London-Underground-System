from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

# Defining the stations and edges as per the initial setup
vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
edges = [
    ('A', 'B', 1), ('A', 'C', 1), ('B', 'D', 1), ('B', 'E', 1),
    ('C', 'D', 1), ('C', 'F', 1), ('D', 'G', 1), ('D', 'E', 1),
    ('E', 'H', 1), ('F', 'G', 1), ('G', 'H', 1), ('H', 'I', 1),
    ('I', 'J', 1)
]

def create_tube_network_stops():
    """
    Creates a tube network graph where each connection (edge) represents a single stop.

    Returns:
        graph: AdjacencyListGraph representing the network.
        vertices: List of station names.
    """
    graph = AdjacencyListGraph(len(vertices), directed=False, weighted=True)
    
    # Adding edges with weight of 1 to represent one stop between stations
    for edge in edges:
        start_idx = vertices.index(edge[0])
        end_idx = vertices.index(edge[1])
        graph.insert_edge(start_idx, end_idx, 1)  # Weight is 1 for each stop
    
    return graph, vertices

def find_shortest_path_by_stops(start_station, end_station):
    """
    Finds the shortest path between two stations based on the number of stops.

    Parameters:
        start_station (str): Name of the starting station.
        end_station (str): Name of the destination station.

    Returns:
        dict: Contains the shortest path as a list of station names and the total number of stops.
    """
    graph, vertices = create_tube_network_stops()
    start_idx = vertices.index(start_station)
    end_idx = vertices.index(end_station)
    
    # Using Dijkstra’s algorithm to find the shortest path in terms of stops
    distances, predecessors = dijkstra(graph, start_idx)
    path = print_path(predecessors, start_idx, end_idx, lambda x: vertices[x])
    
    return {
        'path': path,
        'total_stops': distances[end_idx]
    }

# Testing out the function to find shortest path by number of stops
result = find_shortest_path_by_stops('A', 'J')
print("Shortest path (stops) from A to J:", ' -> '.join(result['path']))
print("Total number of stops:", result['total_stops'])
