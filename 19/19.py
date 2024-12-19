import fileinput
import functools

with fileinput.input() as f:
    lines = iter(f)

    patterns = next(lines).rstrip().split(", ")
    next(lines)
    designs = [line.rstrip() for line in lines]

@functools.cache
def is_design_possible(design: str) -> bool:
    if design == "":
        return True

    return any(is_design_possible(design[len(pat):]) for pat in patterns if design.startswith(pat))

p1_answer = sum(is_design_possible(d) for d in designs)
print(f"p1 answer: {p1_answer}")

# p2

@functools.cache
def count_pat_combos(design: str) -> int:
    if design == "":
        return 1

    return sum(count_pat_combos(design[len(pat):]) for pat in patterns if design.startswith(pat))

p2_answer = sum(count_pat_combos(d) for d in designs)
print(f"p2 answer: {p2_answer}")
