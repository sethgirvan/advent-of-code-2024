from collections import Counter
import fileinput

lines = (line.rstrip() for line in fileinput.input())
pairs = (line.split() for line in lines)
left, right = zip(*pairs)
left = list(map(int, left))
right = list(map(int, right))
left_sorted = sorted(left)
right_sorted = sorted(right)
dists = (abs(l - r) for l, r in zip(left_sorted, right_sorted))
p1_answer = sum(dists)
print(f"p1 answer: {p1_answer}")

# p2

right_counts = Counter(right)

def score(x: int, counts: Counter) -> int:
    return x * counts[x] if x in counts else 0

p2_answer = sum(score(l, right_counts) for l in left)
print(f"p2 answer: {p2_answer}")
