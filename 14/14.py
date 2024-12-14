from collections import Counter
import fileinput
import numpy as np
import re

class Robot:
    position: np.ndarray
    velocity: np.ndarray

    def __init__(self, px: int, py: int, vx: int, vy: int) -> None:
        self.position = np.array([px, py])
        self.velocity = np.array([vx, vy])

def parse_robot(line: str):
    matches = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
    if matches is None:
        raise Exception(f"Failed parsing robot: '{line}'")

    return Robot(int(matches.group(1)), int(matches.group(2)),
                 int(matches.group(3)), int(matches.group(4)))

robots = [parse_robot(line.rstrip()) for line in fileinput.input()]
end_positions = [(r.position + 100 * r.velocity) % np.array([101, 103]) for r in robots]
q1_count = sum(p[0] > 50 and p[1] < 51 for p in end_positions)
q2_count = sum(p[0] < 50 and p[1] < 51 for p in end_positions)
q3_count = sum(p[0] < 50 and p[1] > 51 for p in end_positions)
q4_count = sum(p[0] > 50 and p[1] > 51 for p in end_positions)
p1_answer = q1_count * q2_count * q3_count * q4_count
print(f"p1 answer: {p1_answer}")

# p2

def draw_robots(positions: Counter[tuple[int, int]]) -> None:
    for i in range(103):
        for j in range(101):
            pos = (j, i)
            c = positions[pos] if pos in positions else "."
            print(c, end="")
        print("")

positions = [r.position for r in robots]
position_tups = list(map(tuple, positions))
positions_set = set(map(tuple, positions))
for seconds in range(101 * 103):
    # I guess a Christmas tree should be symmetric about the vertical axis?
    mirrored = (np.array([100 - p[0], p[1]]) for p in positions)
    symmetric_count = sum(tuple(m) in position_tups for m in mirrored)
    if symmetric_count >= 0.2 * len(positions):
        print(f"seconds: {seconds}")
        draw_robots(Counter(position_tups))

    for i, p in enumerate(positions):
        positions[i] = (positions[i] + robots[i].velocity) % np.array([101, 103])
    position_tups = list(map(tuple, positions))
    positions_set = set(map(tuple, positions))
