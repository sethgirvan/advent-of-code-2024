from typing import Generator, Iterable
import fileinput
import re

def count_line(line: str) -> int:
    return len(re.findall(r"XMAS", line)) + len(re.findall(r"SAMX", line))

def count_lines(lines: Iterable[str]) -> int:
    return sum(map(count_line, lines))

def transpose(lines: list[str]) -> list[str]:
    return ["".join(s) for s in zip(*lines)]

def diagonals(lines: list[str]) -> Generator[str, None, None]:
    for i in range(0, len(lines)):
        yield "".join(lines[i - j][j] for j in range(0, i + 1))
    for i in range(1, len(lines)):
        yield "".join(lines[i + len(lines) - 1 - j][j] for j in range(i, len(lines)))

lines = [line.rstrip() for line in fileinput.input()]
verticals = transpose(lines)
northeast = diagonals(lines)
northwest = diagonals(list(reversed(lines)))

p1_answer = count_lines(lines) + count_lines(verticals) + count_lines(northeast) + count_lines(northwest)
print(f"p1 anwser: {p1_answer}")

# p2

# We flatten all lines into one long line with newlines replaced with the '#'
# character. If we are looking for, eg:
#
#   M.S
#   .A.
#   M.S
#
# We know that the first M can be followed by any single character (except a
# newline which we have replaced with '#'), then by the first S. Then since the
# A is on the next line and one place to the left of that S, we know there
# should be exactly 139 (given a 140x140 square of characters) (including the
# '#' character representing the newline) characters in between the S and the A.
#
# Similar logic for there being 139 character between the A and the second M.
#
# We then repeat the search for all four possible variations:

#   M.S    M.M    S.S    S.M
#   .A.    .A.    .A.    .A.
#   M.S    S.S    M.M    M.S

lines = [line.replace("\n", "#") for line in fileinput.input()]
n = len(lines)
flattened = "".join(lines)
regexes = [
        rf"(?=M[^#]S.{{{n-1}}}A.{{{n-1}}}M[^#]S)",
        rf"(?=M[^#]M.{{{n-1}}}A.{{{n-1}}}S[^#]S)",
        rf"(?=S[^#]S.{{{n-1}}}A.{{{n-1}}}M[^#]M)",
        rf"(?=S[^#]M.{{{n-1}}}A.{{{n-1}}}S[^#]M)",
]
p2_answer = sum(len(re.findall(regex, flattened)) for regex in regexes)
print(f"p2 answer: {p2_answer}")
