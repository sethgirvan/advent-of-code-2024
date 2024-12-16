# I thought this was sort of similar to 2023 day 17
# https://adventofcode.com/2023/day/17, where in that case when applying
# Dijkstra's algorithm each "node" in the graph is a tuple of not just the
# position on the grid but also the number of forward moves made so far. In
# today's case a "node" is a tuple of not just the position but also the
# direction we are facing since turning has a cost.

from functools import total_ordering
from typing import Optional

import fileinput
import heapq

grid = [line.rstrip() for line in fileinput.input()]
def grid_loc(loc: complex) -> str:
    return grid[int(loc.real)][int(loc.imag)]

def get_start() -> complex:
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "S":
                return i + 1j * j
    raise Exception("Start not found")

@total_ordering
class ToVisit:
    loc: complex
    direction: complex
    score: int
    # Tuple of previous node's (loc, direction).
    prev: Optional[tuple[complex, complex]]

    def __init__(
            self,
            loc: complex,
            direction: complex,
            score: int,
            prev: Optional[tuple[complex, complex]]
    ) -> None:
        self.loc = loc
        self.direction = direction
        self.score = score
        self.prev = prev

    def __lt__(self, other) -> bool:
        return self.score < other.score

# Maps (loc, direction) to (score, set of previous (loc, directions)s)
visited: dict[tuple[complex, complex], tuple[int, set[Optional[tuple[complex, complex]]]]] = {}
end_prevs: set[tuple[complex, complex]] = set()
heap: list[ToVisit] = []
start = ToVisit(get_start(), 0 + 1j, 0, None)
heapq.heappush(heap, start)
p1_answer: Optional[int] = None
end: Optional[complex] = None

# Dijkstra's algorithm, keeping in mind that we treat all four possible
# directions we could be facing on a given tile in the maze as unique nodes in
# the graph.
#
# For part two we keep track of each visited node's (where a node is a
# (location, direction) tuple) previous node, but as a set of all possible
# previous nodes that reached there with the same (lowest) score.
while len(heap) > 0:
    tile = heapq.heappop(heap)
    if p1_answer is not None and tile.score > p1_answer:
        break
    if (tile.loc, tile.direction) in visited:
        visited_score, visited_prev = visited[(tile.loc, tile.direction)]
        if tile.score == visited_score:
            assert tile.prev is not None
            visited_prev.add(tile.prev)
        continue

    if grid_loc(tile.loc) == "E":
        if p1_answer is None:
            end = tile.loc
            p1_answer = tile.score
            print(f"p1 answer: {p1_answer}")

        assert tile.prev is not None
        end_prevs.add(tile.prev)

        continue

    if grid_loc(tile.loc) == "#":
        continue

    visited[(tile.loc, tile.direction)] = (tile.score, {tile.prev})
    heapq.heappush(heap, ToVisit(tile.loc + tile.direction, tile.direction, tile.score + 1, (tile.loc, tile.direction)))
    # The case of rotating 180 degrees is handled when we visit one of the
    # following ToVisits and subsequently rotate it another 90 degrees.
    heapq.heappush(heap, ToVisit(tile.loc, 1j * tile.direction, tile.score + 1000, (tile.loc, tile.direction)))
    heapq.heappush(heap, ToVisit(tile.loc, -1j * tile.direction, tile.score + 1000, (tile.loc, tile.direction)))

def add_p2_tiles(locdir: Optional[tuple[complex, complex]], p2_tiles: set[complex]) -> None:
    if locdir is None:
        return

    loc, _ = locdir
    p2_tiles.add(loc)
    _, prevs = visited[locdir]
    for prev in prevs:
        add_p2_tiles(prev, p2_tiles)

assert end is not None
p2_tiles: set[complex] = {end}
for end_prev in end_prevs:
    add_p2_tiles(end_prev, p2_tiles)

p2_answer = len(p2_tiles)
print(f"p2 answer: {p2_answer}")
