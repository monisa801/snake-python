from collections import deque
import numpy as np

def get_neighbors(pos, grid_size):
    """Get valid neighboring positions."""
    x, y = pos
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = (x + dx) % grid_size
        new_y = (y + dy) % grid_size
        neighbors.append((new_x, new_y))
    return neighbors

def find_path_bfs(start, target, obstacles, grid_size):
    """
    Find path using Breadth-First Search.
    Returns a list of positions from start to target.
    """
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        (vertex, path) = queue.popleft()
        for next_pos in get_neighbors(vertex, grid_size):
            if next_pos == target:
                return path + [next_pos]
            if next_pos not in visited and next_pos not in obstacles:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    return None

def find_path_dfs(start, target, obstacles, grid_size):
    """
    Find path using Depth-First Search.
    Returns a list of positions from start to target.
    """
    stack = [(start, [start])]
    visited = {start}
    
    while stack:
        (vertex, path) = stack.pop()
        for next_pos in get_neighbors(vertex, grid_size):
            if next_pos == target:
                return path + [next_pos]
            if next_pos not in visited and next_pos not in obstacles:
                visited.add(next_pos)
                stack.append((next_pos, path + [next_pos]))
    return None

def get_next_move(current_pos, target_pos, obstacles, grid_size, algorithm='bfs'):
    """
    Get the next move for the snake using either BFS or DFS.
    Returns the next position to move to.
    """
    if algorithm == 'bfs':
        path = find_path_bfs(current_pos, target_pos, obstacles, grid_size)
    else:
        path = find_path_dfs(current_pos, target_pos, obstacles, grid_size)
    
    if path and len(path) > 1:
        return path[1]  # Return the next position in the path
    return None 