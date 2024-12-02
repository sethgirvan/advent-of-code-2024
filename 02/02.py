import fileinput
import numpy as np

lines = (line.strip() for line in fileinput.input())
reports = [np.fromstring(line, dtype=int, sep=' ') for line in lines]

def is_rpt_safe(rpt: np.ndarray) -> bool:
    diffs = rpt[1:] - rpt[:-1]
    return bool(np.all((-3 <= diffs) & (diffs <= -1)) or np.all((1 <= diffs) & (diffs <= 3)))

p1_answer = sum(map(is_rpt_safe, reports))
print(f"p1 answer: {p1_answer}")

# p2

def is_diff_safe(diff: int, sign: int) -> bool:
    if sign < 0:
        return -3 <= diff and diff <= -1
    return 1 <= diff and diff <= 3

def is_rpt_safe_sign(rpt: np.ndarray, sign: int) -> bool:
    diffs = rpt[1:] - rpt[:-1]
    for i, d in enumerate(diffs[:-1]):
        if not is_diff_safe(d, sign):
            return is_rpt_safe(np.delete(rpt, i)) or is_rpt_safe(np.delete(rpt, i + 1))

    return True

def is_rpt_safe_p2(rpt: np.ndarray) -> bool:
    return is_rpt_safe_sign(rpt, 1) or is_rpt_safe_sign(rpt, -1)

p2_answer = sum(map(is_rpt_safe_p2, reports))
print(f"p2 answer: {p2_answer}")
