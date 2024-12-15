from copy import deepcopy
import fileinput

dir_to_step: dict[str, tuple[int, int]] = {
        "^": (-1, 0),
        "<": (0, -1),
        "v": (1, 0),
        ">": (0, 1),
}

def add_tuples(t1, t2) -> tuple[int, int]:
    return tuple(i1 + i2 for i1, i2 in zip(t1, t2))

grid: list[list[str]] = []
moves: list[tuple[int, int]] = []

with fileinput.input() as f:
    lines = iter(f)
    for line in lines:
        line = line.rstrip()
        if not line:
            break

        grid.append(list(line))

    moves += (dir_to_step[c] for line in lines for c in line.rstrip())

p1_grid = deepcopy(grid)

def find_robot(grid: list[list[str]]) -> tuple[int, int]:
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "@":
                return (i, j)
    raise Exception("Failed to find robot")

def try_move_obj(grid: list[list[str]], pos: tuple[int, int], move: tuple[int, int]) -> bool:
    i, j = pos
    c = grid[i][j]

    if c == ".":
        return True
    if c == "#":
        return False
    if c == "O" or c == "@":
        move_pos = add_tuples(pos, move)
        if try_move_obj(grid, move_pos, move):
            ni, nj = move_pos
            grid[ni][nj] = c
            return True
        else:
            return False

    raise Exception(f"Unexpected character '{c}' at position {pos}")

def move_robot(grid: list[list[str]], pos: tuple[int, int], move: tuple[int, int]) -> tuple[int, int]:
    if try_move_obj(grid, pos, move):
        i, j = pos
        grid[i][j] = "."
        return add_tuples(pos, move)
    return pos

def gps_sum(grid):
    return sum(100 * i + j for i, row in enumerate(grid) for j, c in enumerate(row) if c == "O")

robot_pos = find_robot(p1_grid)
for move in moves:
    robot_pos = move_robot(p1_grid, robot_pos, move)

p1_answer = gps_sum(p1_grid)
print(f"p1 answer: {p1_answer}")

# p2

def square_to_p2(c: str) -> str:
    if c == "@":
        return "@."
    if c == "O":
        return "[]"
    return c + c

p2_grid = [[c2 for c in row for c2 in square_to_p2(c)] for row in grid]

def swap_squares(grid: list[list[str]], p1: tuple[int, int], p2: tuple[int, int]) -> None:
    i1, j1 = p1
    i2, j2 = p2
    grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]

def p2_try_move_obj(grid: list[list[str]], pos: tuple[int, int], move: tuple[int, int], dry_run: bool) -> bool:
    i, j = pos
    c = grid[i][j]

    if c == ".":
        return True
    if c == "#":
        return False
    if c == "@" or (move[0] == 0 and (c == "[" or c == "]")):
        move_pos = add_tuples(pos, move)
        if p2_try_move_obj(grid, move_pos, move, dry_run):
            if not dry_run:
                swap_squares(grid, pos, move_pos)
            return True
        else:
            return False
    if move[0] != 0 and (c == "[" or c == "]"):
        move_pos = add_tuples(pos, move)
        pair_pos = (i, j + 1) if c == "[" else (i, j - 1)
        pair_move_pos = add_tuples(pair_pos, move)
        if dry_run or p2_try_move_obj(grid, pair_move_pos, move, True):
            if (p2_try_move_obj(grid, move_pos, move, dry_run)
                    and p2_try_move_obj(grid, pair_move_pos, move, dry_run)):
                if not dry_run:
                    swap_squares(grid, pos, move_pos)
                    swap_squares(grid, pair_pos, pair_move_pos)

                return True

            return False

        else:
            return False

    raise Exception(f"Unexpected character '{c}' at position {pos}")

def p2_move_robot(grid: list[list[str]], pos: tuple[int, int], move: tuple[int, int]) -> tuple[int, int]:
    if p2_try_move_obj(grid, pos, move, False):
        return add_tuples(pos, move)
    return pos

def p2_gps_sum(grid):
    return sum(100 * i + j for i, row in enumerate(grid) for j, c in enumerate(row) if c == "[")

p2_robot_pos = find_robot(p2_grid)
for move in moves:
    p2_robot_pos = p2_move_robot(p2_grid, p2_robot_pos, move)

p2_answer = p2_gps_sum(p2_grid)
print(f"p2 answer: {p2_answer}")
