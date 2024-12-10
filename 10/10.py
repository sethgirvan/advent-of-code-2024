import fileinput

grid = [[int(c) for c in line.rstrip()] for line in fileinput.input()]

def in_grid(i: int, j: int) -> bool:
    return 0 <= i and i < len(grid) and 0 <= j and j < len(grid[i])

def neighbors(i: int, j: int) -> list[tuple[int, int]]:
    candidates = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
    return [n for n in candidates if in_grid(*n)]

def score(pos: tuple[int, int], height: int, visited: set[tuple[int, int]]) -> int:
    i, j = pos

    if pos in visited:
        return 0
    if grid[i][j] != height:
        return 0

    visited.add(pos)

    if height == 9:
        return 1

    return sum(score(n, height + 1, visited) for n in neighbors(*pos))

p1_answer = sum(score((i, j), 0, set()) for i in range(len(grid)) for j in range(len(grid[i])))
print(f"p1 answer: {p1_answer}")

# p2

def score_p2(pos: tuple[int, int], height: int) -> int:
    i, j = pos

    if grid[i][j] != height:
        return 0

    if height == 9:
        return 1

    return sum(score_p2(n, height + 1) for n in neighbors(*pos))

p2_answer = sum(score_p2((i, j), 0) for i in range(len(grid)) for j in range(len(grid[i])))
print(f"p2 answer: {p2_answer}")
