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
        print("No path found!")
        return []

    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    
    path.append(start)
    path.reverse()
    return path

def print_path(grid, path):
    grid_copy = [row[:] for row in grid]

    for row, col in path:
        grid_copy[row][col] = '*'

    for row in grid_copy:
        print(" ".join(str(cell) for cell in row))