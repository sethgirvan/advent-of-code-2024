from typing import Generator
import fileinput
import numpy as np
import re

def parse_machine(lines: list[str]) -> tuple[np.ndarray, np.ndarray]:
    match_a = re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[0])
    match_b = re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[1])
    match_prize = re.match(r"Prize: X=(\d+), Y=(\d+)", lines[2])
    if match_a is None or match_b is None or match_prize is None:
        raise Exception(f"Failed parsing machine:\n{lines}")

    return (np.array([[int(match_a.group(1)), int(match_b.group(1))],
                     [int(match_a.group(2)), int(match_b.group(2))]]),
            np.array([int(match_prize.group(1)), int(match_prize.group(2))])
            )

def machine_lines() -> Generator[list[str], None, None]:
    with fileinput.input() as f:
        lines = iter(f)
        try:
            while True:
                yield [next(lines).rstrip(), next(lines).rstrip(), next(lines).rstrip()]
                next(lines)
        except(StopIteration):
            return

# cost_p2 also works for p1 and is more efficient than this function. This
# function should work even if machines A and B are collinear, which turns out
# to never be the case.
def cost(machine: tuple[np.ndarray, np.ndarray]) -> int:
    coeff, prize = machine

    costs: list[int] = []
    ax = coeff[0][0]
    ay = coeff[1][0]
    prizex = prize[0]
    prizey = prize[1]
    bx = coeff[0][1]
    by = coeff[1][1]
    for apresses in range(0, 101):
        amovex = apresses * ax
        bmovex = prizex - amovex
        if bmovex < 0:
            break
        if bmovex % bx == 0:
            bpresses = bmovex // bx
            if apresses * ay + bpresses * by == prizey:
                costs.append(3 * apresses + bpresses)

    return min(costs) if len(costs) > 0 else 0

machines = (parse_machine(m) for m in machine_lines())
costs = (cost(m) for m in machines)
p1_answer = sum(costs)
print(f"p1 answer: {p1_answer}")

# p2

def machine_to_p2(machine: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    return (machine[0], machine[1] + 10000000000000)

machines_p2 = (machine_to_p2(parse_machine(m)) for m in machine_lines())

# Relies on machines A and B never being collinear, which is the case in our
# input.
def cost_p2(machine: tuple[np.ndarray, np.ndarray]) -> int:
    coeff, prize = machine
    presses = np.linalg.solve(coeff, prize)
    apress_trunc = int(presses[0])
    bpress_trunc = int(presses[1])
    for apresses in range(apress_trunc, apress_trunc + 2):
        for bpresses in range(bpress_trunc, bpress_trunc + 2):
            if np.array_equal(coeff @ np.array([apresses, bpresses]), prize):
                return 3 * apresses + bpresses
    return 0

costs_p2 = (cost_p2(m) for m in machines_p2)
p2_answer = sum(costs_p2)
print(f"p2 answer: {p2_answer}")
