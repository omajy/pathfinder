import heapq
import math 
from utils import get_neighbours, reconstruct_path, print_path

def euclidean(current_row, current_col, end):
        heuristic = math.sqrt(((current_row-end[0])**2)+((current_col-end[1])**2))
        return heuristic
    
def manhattan(current_row, current_col, end):
        heuristic = (abs(current_row-end[0])+abs(current_col-end[1]))
        return heuristic

def astar(grid, rows, cols, start, end, heuristic="manhattan"):
    heuristic_func = manhattan if heuristic == "manhattan" else euclidean
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
# get euclidean OR
# get manhattan  
# expand node with lowest cost (NOT cumulative) + heuristic (manhattan or euclidean)
# check that nodes neighbours + all other nodes for cheapest
# keep all nodes in queue so we can find cheapest always until we reach end AND end is cheapest node
# always expanding cheapest node and then next cheapest node until end is reached and cheapest (value + heuristic)
# write tests

            if neighbour not in cumulative_cost or new_cost < cumulative_cost[neighbour]:
                cumulative_cost[neighbour] = new_cost 
                priority = new_cost + heuristic_func(neighbour[0], neighbour[1], end)
                heapq.heappush(priority_queue, (new_cost, neighbour))
                parent[neighbour] = (current_row, current_col)

    path = reconstruct_path(parent, start, end)
    print_path(grid, path)
    return path