import fileinput

grid = [line.rstrip() for line in fileinput.input()]

def in_grid(i: int, j: int) -> bool:
    return 0 <= i and i < len(grid) and 0 <= j and j < len(grid[i])

def neighbors(i: int, j: int) -> list[tuple[int, int]]:
    candidates = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
    return [n for n in candidates if in_grid(*n)]

visited = set()

def connected_region(i: int, j: int) -> set[tuple[int, int]]:
    if (i, j) in visited:
        return set()
    visited.add((i, j))

    c = grid[i][j]
    ret = {(i, j)}
    for ni, nj in neighbors(i, j):
        nc = grid[ni][nj]
        if nc == c:
            ret.update(connected_region(ni, nj))

    return ret

def perimeter(region: set[tuple[int, int]]) -> int:
    # Count number of vertical | sections in the perimeter.
    vertical_fences = 0
    for i, line in enumerate(grid):
        was_inside = False
        for j in range(len(line)):
            inside = (i, j) in region
            if inside != was_inside:
                vertical_fences += 1
            was_inside = inside
        if was_inside:
            vertical_fences += 1

    # Count number of horizontal - sections in the perimeter.
    horiz_fences = 0
    for j in range(len(grid[0])):
        was_inside = False
        for i in range(len(grid)):
            inside = (i, j) in region
            if inside != was_inside:
                horiz_fences += 1
            was_inside = inside
        if was_inside:
            horiz_fences += 1

    return vertical_fences + horiz_fences


regions = [connected_region(i, j) for i, line in enumerate(grid) for j in range(len(line)) if (i, j) not in visited]

p1_answer = sum(len(region) * perimeter(region) for region in regions)
print(f"p1 answer: {p1_answer}")

# p2

def is_inside(i, j, region: set[tuple[int, int]]) -> bool:
    return in_grid(i, j) and (i, j) in region

# Number of corners is the same as the number of sides.
def count_corners(region: set[tuple[int, int]]) -> int:
    """
    For each square in the region X, we examine all four corners of that square,
    like so:

      .12  ...  ...  23.
      .X3  .X1  3X.  1X.
      ...  .32  21.  ...

    Where X is the square we are examining, and the variables n1, n2, and n3 are
    the coordinates of the squares marked 1, 2, and 3 respectively. If 1 and 3
    are both not in the region, that is an outside corner, for example, when
    checking the top right corner of the square

      .12
      .X3
      ...

    This counts as an outside corner (where 'O's are not in the region and '.'
    can be either inside or outside the region):

      .O.
      .XO
      ...

    And this counts as an inside corner:

      .XO
      .XX
      ...

    """
    corners = 0
    for i, j in region:
        corner_neighbors = [
            ((i - 1, j), (i - 1, j + 1), (i, j + 1)),
            ((i, j + 1), (i + 1, j + 1), (i + 1, j)),
            ((i + 1, j), (i + 1, j - 1), (i, j - 1)),
            ((i, j - 1), (i - 1, j - 1), (i - 1, j)),
        ]
        for n1, n2, n3 in corner_neighbors:
            if not is_inside(*n1, region) and not is_inside(*n3, region):
                # Outside corner
                corners += 1
            if is_inside(*n1, region) and not is_inside(*n2, region) and is_inside(*n3, region):
                # Inside corner
                corners += 1

    return corners

p2_answer = sum(len(region) * count_corners(region) for region in regions)
print(f"p2 answer: {p2_answer}")
