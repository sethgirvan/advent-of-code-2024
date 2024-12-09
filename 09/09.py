import fileinput

line = next(fileinput.input()).rstrip()

file_segs: list[tuple[int, int]] = []
try:
    id = 0
    lineiter = iter(line)
    for c in lineiter:
        file_segs.append((id, int(c)))
        free_space = next(lineiter)
        file_segs.append((-1, int(free_space)))
        id += 1
except StopIteration:
    pass

file_segs_p1 = file_segs.copy()
compacted: list[tuple[int, int]] = []
def compact_disk():
    left = 0
    right = len(file_segs_p1) - 1
    while left <= right:
        id, length = file_segs_p1[left]
        if id == -1:
            while length > 0:
                tomove_id, tomove_len = file_segs_p1[right]
                if tomove_id == -1:
                    right -= 1
                    if left == right:
                        return
                    continue

                movelen = min(tomove_len, length)
                compacted.append((tomove_id, movelen))

                if movelen == tomove_len:
                    right -= 1
                    if left == right:
                        return
                else:
                    file_segs_p1[right] = (tomove_id, tomove_len - movelen)

                length -= movelen
        else:
            compacted.append((id, length))

        left += 1

def disk_hash(disk: list[tuple[int, int]]) -> int:
    hash = 0
    pos = 0

    for id, length in disk:
        if (id >= 0):
            end = pos + length - 1
            pos_sum = end * (end + 1) // 2
            if pos > 0:
                pos_sum -= (pos - 1) * pos // 2

            hash += id * pos_sum
        pos += length

    return hash

compact_disk()

p1_answer = disk_hash(compacted)
print(f"p1 answer: {p1_answer}")

# p2

file_segs_p2 = file_segs.copy()
def compact_p2():
    left = 0
    while left < len(file_segs_p2):
        id, length = file_segs_p2[left]
        if id == -1:
            for right in range(len(file_segs_p2) - 1, left, -1):
                tomove_id, tomove_len = file_segs_p2[right]
                if tomove_id == -1 or tomove_len > length:
                    continue

                file_segs_p2[right] = (-1, tomove_len)
                if (tomove_len == length):
                    file_segs_p2[left] = (tomove_id, tomove_len)
                else:
                    file_segs_p2[left] = (-1, length - tomove_len)
                    file_segs_p2.insert(left, (tomove_id, tomove_len))
                break
        left += 1

compact_p2()
p2_answer = disk_hash(file_segs_p2)
print(f"p2 answer: {p2_answer}")
