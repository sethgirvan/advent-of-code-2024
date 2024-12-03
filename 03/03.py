from typing import Iterable
import fileinput
import re

def p1(lines: Iterable[str]) -> int:
    ixs_nested = (re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', line) for line in lines)
    ixs = ((int(l), int(r)) for ixline in ixs_nested for l, r in ixline)
    products = (l * r for l, r in ixs)
    return sum(products)

p1_answer = p1(fileinput.input())
print(f"p1_answer: {p1_answer}")

# p2

fragments = []
do = True
for line in fileinput.input():
    while len(line) > 0:
        if do:
            match = re.search(r"don't\(\)", line)
            if match is not None:
                fragments.append(line[:match.start()])
                line = line[match.end():]
                do = False
            else:
                fragments.append(line)
                break
        else:
            match = re.search(r"do\(\)", line)
            if match is not None:
                line = line[match.end():]
                do = True
            else:
                break

p2_answer = p1(fragments)
print(f"p2_answer: {p2_answer}")
