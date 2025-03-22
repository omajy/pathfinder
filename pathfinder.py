STUDENT_ID = 'a1850943'
DEGREE = 'UG'

from collections import deque
import heapq
from utils import load_map, get_neighbours, reconstruct_path, print_path
from bfs import bfs
from ucs import ucs
from astar import astar

grid, start, end, (rows, cols) = load_map('map.txt')
bfs(grid, rows, cols, start, end)
print(" ")
ucs(grid, rows, cols, start, end)
print(" ")
print("manhattan")
astar(grid, rows, cols, start, end)
print(" ")
print("euclidean")
astar(grid, rows, cols, start, end, heuristic="euclidean")

