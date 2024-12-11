import fileinput
import functools
import math

stones = list(map(int, next(fileinput.input()).rstrip().split()))

@functools.cache
def num_stones_after_blinks(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return num_stones_after_blinks(1, blinks - 1)

    digits = int(math.log10(stone)) + 1
    if digits % 2 == 0:
        divisor = 10 ** (digits // 2)
        left = stone // divisor
        right = stone % divisor

        return num_stones_after_blinks(left, blinks - 1) + num_stones_after_blinks(right, blinks - 1)

    return num_stones_after_blinks(stone * 2024, blinks - 1)

p1_answer = sum(num_stones_after_blinks(stone, 25) for stone in stones)
print(f"p1 answer: {p1_answer}")

# p2

p2_answer = sum(num_stones_after_blinks(stone, 75) for stone in stones)
print(f"p2 answer: {p2_answer}")
