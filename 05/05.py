from functools import cmp_to_key
import fileinput

comes_after: dict[int, set[int]] = {}
rules: set[tuple[int, int]] = set()

def check_line(page_nrs: list[int]) -> int:
    valid = all((x not in comes_after) or (len(comes_after[x] & set(page_nrs[0:i])) == 0) for i, x in enumerate(page_nrs))
    return page_nrs[len(page_nrs) // 2] if valid else 0

def compare_page_nrs(x, y) -> int:
    if (x, y) in rules:
        return -1
    elif (y, x) in rules:
        return 1
    return 0

with fileinput.input() as f:
    lines = iter(f)
    for line in lines:
        if not line.rstrip():
            break

        before, after = map(int, line.split("|"))
        rules.add((before, after))
        if before not in comes_after:
            comes_after[before] = set()
        comes_after[before].add(after)

    updates = [list(map(int, line.split(","))) for line in lines]
    p1_answer = sum(check_line(line) for line in updates)
    print(f"p1 answer: {p1_answer}")

incorrect_updates = [line for line in updates if not check_line(line)]
corrected = [sorted(u, key=cmp_to_key(compare_page_nrs)) for u in incorrect_updates]
p2_answer = sum(u[len(u) // 2] for u in corrected)
print(f"p2 answer: {p2_answer}")
