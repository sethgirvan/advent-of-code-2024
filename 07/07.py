import fileinput
import math

def exists_valid_equation(operands: list[int], result: int):
    if len(operands) == 1:
        return operands[0] == result

    last = operands[-1]
    return (exists_valid_equation(operands[:-1], result - last)
            or (result % last == 0 and exists_valid_equation(operands[:-1], result // last)))

resultstrs, opstrs = zip(*(line.rstrip().split(":") for line in fileinput.input()))
results = list(map(int, resultstrs))
opslist = [list(map(int, ops.split())) for ops in opstrs]

p1_answer = sum(result for result, ops in zip(results, opslist) if exists_valid_equation(ops, result))
print(f"p1_answer: {p1_answer}")

# p2

def p2_exists_valid_equation(operands: list[int], result: int):
    if len(operands) == 1:
        return operands[0] == result

    last = operands[-1]
    mod = int(10 ** (int(math.log10(last)) + 1))
    return (p2_exists_valid_equation(operands[:-1], result - last)
            or (result % last == 0 and p2_exists_valid_equation(operands[:-1], result // last))
            or (result % mod == last and p2_exists_valid_equation(operands[:-1], result // mod)))


p2_answer = sum(result for result, ops in zip(results, opslist) if p2_exists_valid_equation(ops, result))
print(f"p2_answer: {p2_answer}")
