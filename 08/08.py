import fileinput
import math
import operator

grid: list[str] = [line.rstrip() for line in fileinput.input()]

antennas: dict[str, set[tuple[int, int]]] = {}
height = len(grid)
width = len(grid[0])

def in_grid(i: int, j: int) -> bool:
    return 0 <= i and i < height and 0 <= j and j < width

for i, line in enumerate(grid):
    for j, c in enumerate(line):
        if c != ".":
            if c not in antennas:
                antennas[c] = set()
            antennas[c].add((i, j))

antinodes: set[tuple[int, int]] = set()

for locs in antennas.values():
    loclist = list(locs)
    for k, loc1 in enumerate(loclist[:-1]):
        for loc2 in loclist[k + 1:]:
            delta = tuple(map(operator.sub, loc2, loc1))
            an1 = tuple(map(operator.sub, loc1, delta))
            if in_grid(*an1):
                antinodes.add(an1)
            an2 = tuple(map(operator.add, loc2, delta))
            if in_grid(*an2):
                antinodes.add(an2)

p1_answer = len(antinodes)
print(f"p1 answer: {p1_answer}")

# p2

antinodes_p2: set[tuple[int, int]] = set()

for locs in antennas.values():
    loclist = list(locs)
    for k, loc1 in enumerate(loclist[:-1]):
        for loc2 in loclist[k + 1:]:
            delta = tuple(map(operator.sub, loc2, loc1))
            if delta[0] == 0:
                delta_reduced = (0, 1)
            elif delta[1] == 0:
                delta_reduced = (1, 0)
            else:
                delta_gcf = math.gcd(*delta)
                delta_reduced = tuple(x // delta_gcf for x in delta)

            an = loc1
            while(in_grid(*an)):
                antinodes_p2.add(an)
                an = tuple(map(operator.sub, an, delta_reduced))

            an = loc1
            while True:
                an = tuple(map(operator.add, an, delta_reduced))
                if not in_grid(*an):
                    break
                antinodes_p2.add(an)

p2_answer = len(antinodes_p2)
print(f"p2 answer: {p2_answer}")
