from collections import deque
import heapq
import time
import random
from maze import ROWS, COLS,get_neighbors


random.seed(42)
node_costs = {
    (c, r): random.randint(1, 20)
    for c in range(COLS)
    for r in range(ROWS)    
}

def get_path_between(start_pos, end_pos, parent_map):
    
    if start_pos == end_pos:
        return []
    
    # Build path from start_pos to root
    path_from_start = []
    current = start_pos
    while current is not None:
        path_from_start.append(current)
        current = parent_map.get(current)
    
    # Build path from end_pos to root
    path_from_end = []
    current = end_pos
    while current is not None:
        path_from_end.append(current)
        current = parent_map.get(current)
    
    # Find common ancestor (lowest common ancestor)
    path_from_start_set = set(path_from_start)
    common_ancestor = None
    for node in path_from_end:
        if node in path_from_start_set:
            common_ancestor = node
            break
    
    if common_ancestor is None:
        return []
    
    # Build backtrack path: start -> common ancestor
    backtrack_path = []
    current = start_pos
    while current != common_ancestor:
        current = parent_map.get(current)
        if current is not None:
            backtrack_path.append(current)
    
    # Build forward path: common ancestor -> end
    forward_path = []
    current = end_pos
    while current != common_ancestor:
        forward_path.append(current)
        current = parent_map.get(current)
    forward_path.reverse()
    
    # Combine paths
    return backtrack_path + forward_path

def handle_goal_reached(
    current,
    goal,
    parent_map,
    discovered_nodes,
    movement_sequence,
    algo_name,
    path_label
):
    

    # Reconstruct path
    final_path = []
    temp = current
    while temp is not None:
        final_path.append(temp)
        temp = parent_map[temp]
    final_path.reverse()

    return movement_sequence, discovered_nodes, final_path

def bfs(start, goal,):

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    movement_sequence = [start]
    discovered_nodes = {start}
    current_position = start

    while queue:
        current = queue.popleft()

        if current_position != current:
            path_to_current = get_path_between(current_position, current, parent)
            movement_sequence.extend(path_to_current)
            current_position = current
            

        if current == goal:
            return handle_goal_reached(
                current=current,
                goal=goal,
                parent_map=parent,
                discovered_nodes=discovered_nodes,
                movement_sequence=movement_sequence,
                algo_name="BFS",
                path_label="Shortest path length"
            )

        for neighbor in get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                discovered_nodes.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                
    return movement_sequence, discovered_nodes, []

def dfs(start, goal):

    stack = [start]
    visited = {start}
    parent = {start: None}

    movement_sequence = [start]
    discovered_nodes = {start}
    current_position = start

    while stack:
        current = stack.pop()

        if current_position != current:
            path = get_path_between(current_position, current, parent)
            movement_sequence.extend(path)
            current_position = current

        if current == goal:
            return handle_goal_reached(
                current=current,
                goal=goal,
                parent_map=parent,
                discovered_nodes=discovered_nodes,
                movement_sequence=movement_sequence,
                algo_name="DFS",
                path_label="Shortest path length"
            )

        for neighbor in reversed(get_neighbors(current[0], current[1])):
            if neighbor not in visited:
                visited.add(neighbor)
                discovered_nodes.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor) 
                  
    return movement_sequence, discovered_nodes, []            

def ids(start, goal):

    movement_sequence = [start]
    discovered_nodes = set()
    current_position = start

   
    def dls(node, depth_limit, parent, visited):
        nonlocal movement_sequence, discovered_nodes, current_position

        discovered_nodes.add(node)

        if current_position != node:
            path = get_path_between(current_position, node, parent)
            movement_sequence.extend(path)
            current_position = node

        if node == goal:
            return True

        if depth_limit == 0:
            return False

        for neighbor in get_neighbors(node[0], node[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                if dls(neighbor, depth_limit - 1, parent, visited):
                    return True

        return False
    
    max_depth = ROWS * COLS

    for depth in range(max_depth):
        parent = {start: None}          
        visited = {start}
        current_position = start

        if dls(start, depth, parent, visited):
            return handle_goal_reached(
                current=goal,
                goal=goal,
                parent_map=parent,
                discovered_nodes=discovered_nodes,
                movement_sequence=movement_sequence,
                algo_name="IDS",
                path_label="Path length"
            )

    return movement_sequence, discovered_nodes, []

def ucs(start, goal):

    priority_queue = [(0, start)]
    visited = set()
    parent = {start: None}
    g_cost = {start: 0}

    movement_sequence = [start]
    discovered_nodes = {start}
    current_position = start

    while priority_queue:
        cost, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current_position != current:
            path = get_path_between(current_position, current, parent)
            movement_sequence.extend(path)
            current_position = current

        if current == goal:
            return handle_goal_reached(
                current=current,
                goal=goal,
                parent_map=parent,
                discovered_nodes=discovered_nodes,
                movement_sequence=movement_sequence,
                algo_name="UCS",
                path_label="Path to goal"
            )

        for neighbor in get_neighbors(current[0], current[1]):
            step_cost = node_costs[neighbor]     
            new_cost = g_cost[current] + step_cost
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(priority_queue, (new_cost, neighbor))
                discovered_nodes.add(neighbor)
                
    return movement_sequence, discovered_nodes, []

        
def heuristic(a, b):
    # a = (x1, y1), b = (x2, y2)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal):
    
    priority_queue = []
    priority_queue = [(0, start)]

    parent = {start: None}
    g_cost = {start: 0}

    visited = set()
    discovered_nodes = {start}
    movement_sequence = [start]
    current_position = start

    while priority_queue:
        f_cost, current = heapq.heappop(priority_queue)

        if current in visited:
            continue
        visited.add(current)

        if current_position != current:
            path = get_path_between(current_position, current, parent)
            movement_sequence.extend(path)
            current_position = current

        if current == goal:
            return handle_goal_reached(
                current=current,
                goal=goal,
                parent_map=parent,
                discovered_nodes=discovered_nodes,
                movement_sequence=movement_sequence,
                algo_name="A*",
                path_label="Optimal path length"
            )

        for neighbor in get_neighbors(current[0], current[1]):
            step_cost = node_costs[neighbor]
            new_cost = g_cost[current] + step_cost

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                parent[neighbor] = current

                h = heuristic(neighbor, goal)
                f = new_cost + h

                heapq.heappush(priority_queue, (f, neighbor))
                discovered_nodes.add(neighbor)
                
    return movement_sequence, discovered_nodes, []

def hill_climbing(start, goal):
       
    current = start
    movement_sequence = [current]
    discovered_nodes = {current}
    parent = {current: None}

    while current != goal:
        neighbors = get_neighbors(current[0], current[1])
        neighbors = [n for n in neighbors if n not in discovered_nodes]
        if not neighbors:
            break
        next_node = min(neighbors, key=lambda n: heuristic(n, goal))
        parent[next_node] = current
        discovered_nodes.add(next_node)
        movement_sequence.append(next_node)
        current = next_node

    if current == goal:
        return handle_goal_reached(
            current=current,
            goal=goal,
            parent_map=parent,
            discovered_nodes=discovered_nodes,
            movement_sequence=movement_sequence,
            algo_name="Hill Climbing",
            path_label="Path length"
        )
    return movement_sequence, discovered_nodes, []


def get_algorithm_stats(discovered_nodes, movement_sequence, final_path,execution_time=0):
    """Return statistics for comparison"""
    return {
        "nodes_explored": len(discovered_nodes),
        "total_movements": len(movement_sequence),
        "path_length": len(final_path),
        "execution_time": execution_time
    }
    