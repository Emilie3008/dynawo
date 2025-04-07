
import re


def remove_disconnected_lines(graph, disconnected_lines):
    cleaned_graph = {}
    for bus, neighbors in graph.items():
        cleaned_graph[bus] = {
            neighbor: line_id 
            for neighbor, line_id in neighbors.items() 
            if line_id not in disconnected_lines}
    return cleaned_graph

def dfs_with_lines(start_bus, graph):
    visited = []
    stack = [start_bus]
    while stack:
        bus = stack.pop()
        if bus not in visited:
            visited.append(bus)
            for neighbor, lines in graph.get(bus, {}).items():
                if neighbor not in visited:
                    stack += [neighbor, lines]
    if "connected" in visited:
        visited.remove("connected")
    return visited


def get_priority(element):
    # Ordre des motifs (du plus prioritaire au moins prioritaire)
    patterns = [
        (r"L-\d+-\d+-1", 0),
        (r"T-\d+-\d+-1", 1),
        (r"B\d+-L1", 2),         
        (r"B\d+-SH 1", 3),
        (r"B\d+-G1", 4),                
        (r"VL\d+", 5)             
    ]
    for pattern, poids in patterns:
        if re.fullmatch(pattern, element): 
            return poids
    return float('inf') 

def retrieve_islands(graph):
    visited = set()
    components = []
    for bus in graph:
        if bus not in visited:
            component = dfs_with_lines(bus, graph)
            component = sorted(component, key=get_priority)
            components.append(component)
            visited.update(component)
    return components



def subgrid_from_grid(main_grid, elements_to_exclude):

    subgrid = {}
    
    for bus, connections in main_grid.items():
        if bus not in elements_to_exclude:
            subgrid[bus] = {}
            
            for connected_element, link_name in connections.items():
                if (connected_element not in elements_to_exclude and 
                    link_name not in elements_to_exclude):
                    subgrid[bus][connected_element] = link_name
    return subgrid


