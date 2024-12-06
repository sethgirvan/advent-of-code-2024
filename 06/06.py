import fileinput
import numpy as np

grid = [list(line.rstrip()) for line in fileinput.input()]

def in_grid(loc: np.ndarray) -> bool:
    return (0 <= loc[0] and loc[0] < len(grid)
            and 0 <= loc[1] and loc[1] < len(grid[loc[0]]))

def print_grid() -> None:
    for line in grid:
        print("".join(line))
    print("\n")

def get_start() -> np.ndarray:
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "^":
                return np.array([i, j])
    raise Exception("Start not found")
start = get_start()

visited: set[tuple[int, int]] = set()
def patrol() -> bool:
    visited_dirs: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    loc = start
    dir = np.array([-1, 0])
    rot_90_cw = np.array([[0, 1],
                          [-1, 0]])
    while True:
        if (tuple(loc), tuple(dir)) in visited_dirs:
            return True
        visited.add(tuple(loc))
        visited_dirs.add((tuple(loc), tuple(dir)))
        while True:
            next = loc + dir
            if not in_grid(next):
                return False
            if grid[next[0]][next[1]] != "#":
                loc = next
                break
            dir = rot_90_cw @ dir

patrol()
visited_orig = visited.copy()
p1_answer = len(visited)
print(f"p1 answer: {p1_answer}")

# p2

p2_answer = 0
for i, j in visited_orig:
    c = grid[i][j]
    if c != "#":
        orig = c
        grid[i][j] = "#"
        if patrol():
            p2_answer += 1
        grid[i][j] = orig

print(f"p2 answer: {p2_answer}")
