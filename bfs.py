from collections import deque 
from utils import get_neighbours, reconstruct_path, print_path
def bfs(grid, rows, cols, start, end):
    queue = deque([start]) 
    visited = set([start])
    parent = {}

    while queue:
        current_row, current_col = queue.popleft()

        if (current_row, current_col) == end:
            break

        for neighbour in get_neighbours(current_row, current_col, rows, cols, grid):
            if neighbour not in visited:
                queue.append(neighbour)
                visited.add(neighbour)
                parent[neighbour] = (current_row, current_col)

    path = reconstruct_path(parent, start, end)
    print_path(grid, path)
    return path