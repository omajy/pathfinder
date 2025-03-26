STUDENT_ID = 'a1850943'
DEGREE = 'UG'

import sys
from collections import deque 
import heapq
import math

class Utils:
    def load_map(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].split())
        start = tuple(map(int, lines[1].split()))
        end = tuple(map(int, lines[2].split()))

        start = (start[0] - 1, start[1] - 1)
        end = (end[0] - 1, end[1] - 1)

        grid = [
            [int(cell) if cell.isdigit() else cell for cell in line.split()]
            for line in lines[3:]
        ]

        return grid, start, end, (rows, cols)

    def get_neighbours(current_row, current_col, rows, cols, grid):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbours = []

        for row_change, col_change in directions:
            neighbour_row = current_row + row_change
            neighbour_col = current_col + col_change

            if 0 <= neighbour_row < rows and 0 <= neighbour_col < cols:
                if grid[neighbour_row][neighbour_col] != 'X':  
                    neighbours.append((neighbour_row, neighbour_col))
        
        return neighbours

    def reconstruct_path(parent, start, end):
        if end not in parent:
            return []

        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]
        
        path.append(start)
        return path[::-1]  

    def print_path(grid, path):
        grid_copy = [row[:] for row in grid]

        for row, col in path:
            grid_copy[row][col] = '*'

        for row in grid_copy:
            print(" ".join(str(cell) for cell in row))

    def print_visit_counts(grid, visit_counts):
        rows, cols = len(grid), len(grid[0])
        visit_grid = [['.' for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 'X':
                    visit_grid[i][j] = 'X'
        
        for (row, col), count in visit_counts.items():
            visit_grid[row][col] = str(count)
        
        print("#visited")
        for row in visit_grid:
            print(" ".join(str(cell) for cell in row))

class BFS:
    def bfs(grid, rows, cols, start, end):
        queue = deque([start]) 
        visited = set([start])
        parent = {}
        visit_counts = {start: 1} 
        
        while queue:
            current_row, current_col = queue.popleft()

            if (current_row, current_col) == end:
                break

            for neighbour in Utils.get_neighbours(current_row, current_col, rows, cols, grid):
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)
                    parent[neighbour] = (current_row, current_col)
                    visit_counts[neighbour] = 1
                else:
                    visit_counts[neighbour] = visit_counts.get(neighbour, 0) + 1

        path = Utils.reconstruct_path(parent, start, end)
        return path, visit_counts

class UCS:
    def ucs(grid, rows, cols, start, end):
        discovery_time = 0
        priority_queue = [(0, discovery_time, start)]
        heapq.heapify(priority_queue)
        
        cumulative_cost = {start: 0}
        parent = {}
        visit_counts = {start: 1}
        visited = set()

        while priority_queue:
            current_cost, _, (current_row, current_col) = heapq.heappop(priority_queue)
            current = (current_row, current_col)

            if current in visited:
                continue

            visited.add(current)

            if current == end:
                break

            for neighbour in Utils.get_neighbours(current_row, current_col, rows, cols, grid):
                visit_counts[neighbour] = visit_counts.get(neighbour, 0) + 1
                
                current_elevation = grid[current_row][current_col]
                neighbour_elevation = grid[neighbour[0]][neighbour[1]]
                elevation_diff = neighbour_elevation - current_elevation
                
                edge_cost = 1 if elevation_diff <= 0 else 1 + elevation_diff
                new_cost = cumulative_cost[current] + edge_cost
                
                if neighbour not in cumulative_cost or new_cost < cumulative_cost[neighbour]:
                    cumulative_cost[neighbour] = new_cost
                    discovery_time += 1
                    heapq.heappush(priority_queue, (new_cost, discovery_time, neighbour))
                    parent[neighbour] = current

        path = Utils.reconstruct_path(parent, start, end)
        return path, visit_counts

class AStar:
    def euclidean(current_row, current_col, end):
        heuristic = math.sqrt(((current_row-end[0])**2)+((current_col-end[1])**2))
        return heuristic
    
    def manhattan(current_row, current_col, end):
        heuristic = (abs(current_row-end[0])+abs(current_col-end[1]))
        return heuristic

    def astar(grid, rows, cols, start, end, heuristic="manhattan"):
        heuristic_func = AStar.manhattan if heuristic == "manhattan" else AStar.euclidean
        discovery_time = 0
        priority_queue = [(0, discovery_time, start)]
        heapq.heapify(priority_queue)
        
        cumulative_cost = {start: 0}
        parent = {}
        visit_counts = {start: 1}
        visited = set()

        while priority_queue:
            current_cost, _, (current_row, current_col) = heapq.heappop(priority_queue)
            current = (current_row, current_col)

            if current in visited:
                continue

            visited.add(current)

            if current == end:
                break

            for neighbour in Utils.get_neighbours(current_row, current_col, rows, cols, grid):
                visit_counts[neighbour] = visit_counts.get(neighbour, 0) + 1
                
                current_elevation = grid[current_row][current_col]
                neighbour_elevation = grid[neighbour[0]][neighbour[1]]
                elevation_diff = neighbour_elevation - current_elevation
                
                edge_cost = 1 if elevation_diff <= 0 else 1 + elevation_diff
                new_cost = cumulative_cost[current] + edge_cost
                
                if neighbour not in cumulative_cost or new_cost < cumulative_cost[neighbour]:
                    cumulative_cost[neighbour] = new_cost
                    priority = new_cost + heuristic_func(neighbour[0], neighbour[1], end)
                    discovery_time += 1
                    heapq.heappush(priority_queue, (priority, discovery_time, neighbour))
                    parent[neighbour] = current

        path = Utils.reconstruct_path(parent, start, end)
        return path, visit_counts

def main():
    mode = sys.argv[1] 
    input_map = sys.argv[2] 
    algorithm = sys.argv[3]
    if algorithm == "astar":
        heuristic = sys.argv[4] 
    grid, start, end, (rows, cols) = Utils.load_map(input_map)
    
    if mode=='release':
        if algorithm == "bfs":
            path, _ = BFS.bfs(grid, rows, cols, start, end)
        elif algorithm == "ucs":
            path, _ = UCS.ucs(grid, rows, cols, start, end)
        elif algorithm == "astar" and heuristic == "manhattan":
            path, _ = AStar.astar(grid, rows, cols, start, end, heuristic='manhattan')
        elif algorithm == "astar" and heuristic == "euclidean":
            path, _ = AStar.astar(grid, rows, cols, start, end, heuristic='euclidean')
        if path != []:
            Utils.print_path(grid,path)
        else:
            print("null")
            
    if mode == "debug":
        if algorithm == "bfs":
            path, visit_counts = BFS.bfs(grid, rows, cols, start, end)
        elif algorithm == "ucs":
            path, visit_counts = UCS.ucs(grid, rows, cols, start, end)
        elif algorithm == "astar" and heuristic == "manhattan":
            path, visit_counts = AStar.astar(grid, rows, cols, start, end, heuristic='manhattan')
        elif algorithm == "astar" and heuristic == "euclidean":
            path, visit_counts = AStar.astar(grid, rows, cols, start, end, heuristic='euclidean')
        if path != []:
            print('path:')
            Utils.print_path(grid, path) 
        else:
            print("null")
        Utils.print_visit_counts(grid, visit_counts)

if __name__ == "__main__":
    main()
