from collections import deque
from functools import cmp_to_key
import fileinput

GRID_WIDTH = 71
GRID_HEIGHT = 71

def in_grid(x: int, y: int) -> bool:
    return 0 <= x and x < GRID_WIDTH and 0 <= y and y < GRID_HEIGHT

def neighbors(x: int, y: int) -> list[tuple[int, int]]:
    candidates = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    return [n for n in candidates if in_grid(*n)]

def parse_coord(line: str) -> tuple[int, int]:
    return tuple(map(int, line.split(",")))

byte_coords = [parse_coord(line.rstrip()) for line in fileinput.input()]

def p1(fallen_coords: list[tuple[int, int]]) -> int:
    visited: set[tuple[int, int]] = set()
    bfs_queue: deque[tuple[int, tuple[int, int]]] = deque([(0, (0, 0))])
    while len(bfs_queue) > 0:
        steps, coord = bfs_queue.popleft()
        if coord in visited or coord in fallen_coords:
            continue
        if coord == (GRID_WIDTH - 1, GRID_HEIGHT - 1):
            return steps
        visited.add(coord)

        bfs_queue.extend((steps + 1, n) for n in neighbors(*coord))

    raise Exception("Failed to reach exit")

coords_1024 = {*byte_coords[:1024]}
p1_answer = p1(coords_1024)
print(f"p1 answer: {p1_answer}")

# p2

# Binary search for first index at which we cannot reach the exit
l = 0
r = len(byte_coords) - 1
while l < r:
    mid = l + (r - l) // 2
    try:
        p1(byte_coords[:mid + 1])
        l = mid + 1
    except:
        r = mid

p2_answer = ",".join(map(str, byte_coords[l]))
print(f"p2 answer: {p2_answer}")
