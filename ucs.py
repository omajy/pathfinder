import heapq
from utils import get_neighbours, reconstruct_path, print_path

def ucs(grid, rows, cols, start, end):
    priority_queue = [(0, start)]
    heapq.heapify(priority_queue)
    
    cumulative_cost = {start: 0}
    parent = {}

    while priority_queue:
        current_cost, (current_row, current_col) = heapq.heappop(priority_queue)

        if (current_row, current_col) == end:
            break

        for neighbour in get_neighbours(current_row, current_col, rows, cols, grid):
            new_cost = cumulative_cost[(current_row, current_col)] + grid[neighbour[0]][neighbour[1]]
            if grid[neighbour[0]][neighbour[1]] < grid[current_row][current_col]:
                new_cost = cumulative_cost[(current_row, current_col)] + 1

            if neighbour not in cumulative_cost or new_cost < cumulative_cost[neighbour]:
                cumulative_cost[neighbour] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbour))
                parent[neighbour] = (current_row, current_col)

    path = reconstruct_path(parent, start, end) 
    print_path(grid, path)
    return path