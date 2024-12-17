import fileinput

class Regs:
    # regs[0] is register A
    # regs[1] is register B
    # regs[2] is register C
    regs: list[int] 

    def __init__(self, A: int, B: int, C: int) -> None:
        self.regs = [A, B, C]

    def __getitem__(self, index: int) -> int:
        return self.regs[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.regs[index] = value

    @property
    def A(self):
        return self.regs[0]
    @A.setter
    def A(self, value):
        self.regs[0] = value

    @property
    def B(self):
        return self.regs[1]
    @B.setter
    def B(self, value):
        self.regs[1] = value

    @property
    def C(self):
        return self.regs[2]
    @C.setter
    def C(self, value):
        self.regs[2] = value

class Computer:
    regs: Regs
    pc: int
    output: list[int]

    def __init__(self, A: int, B: int, C: int) -> None:
        self.regs = Regs(A, B, C)
        self.pc = 0
        self.output = []

    def combo_val(self, combo: int) -> int:
        if combo <= 3:
            return combo
        if combo >= 7:
            raise Exception(f"Got combo value {combo}")

        return self.regs[combo - 4]

    def adv(self, combo: int) -> None:
        self.regs.A = self.regs.A // (2**self.combo_val(combo))
    def bxl(self, literal: int) -> None:
        self.regs.B ^= literal
    def bst(self, combo: int) -> None:
        self.regs.B = self.combo_val(combo) % 8
    def jnz(self, literal: int) -> None:
        if self.regs.A != 0:
            self.pc = literal
    def bxc(self, _) -> None:
        self.regs.B ^= self.regs.C
    def out(self, combo: int) -> None:
        self.output.append(self.combo_val(combo) % 8)
    def bdv(self, combo: int) -> None:
        self.regs.B = self.regs.A // (2**self.combo_val(combo))
    def cdv(self, combo: int) -> None:
        self.regs.C = self.regs.A // (2**self.combo_val(combo))

    ixs = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

    def execute(self, program: list[int]):
        while self.pc < len(program):
            ix, operand = program[self.pc], program[self.pc + 1]
            self.pc += 2
            if ix >= len(self.ixs):
                raise Exception(f"Out of range instruction {ix},{operand}")
            self.ixs[ix](self, operand)

    def output_str(self) -> str:
        return ",".join(map(str, self.output))

with fileinput.input() as f:
    lines = iter(f)
    A: int = int(next(lines).rstrip().split()[2])
    B: int = int(next(lines).rstrip().split()[2])
    C: int = int(next(lines).rstrip().split()[2])
    next(lines)
    program: list[int] = list(map(int, next(lines).rstrip().split()[1].split(",")))

computer = Computer(A, B, C)
computer.execute(program)
p1_answer = computer.output_str()
print(f"p1 answer: {p1_answer}")

# p2

# My program is
#   Program: 2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0
# If we follow one iteration of the loop (the final '3,0' instruction loops back
# to the beginning when A is nonzero), the registers take on these values with
# respect to the starting value of A, called here A0:
#
#   00: B = A0 % 8
#   02: B = (A0 % 8) ^ 2
#   04: C = A0 // 2**((A0 % 8) ^ 2)
#   06: A = A0 // 8
#   08: B = (A0 % 8) ^ 2 ^ 7
#   10: B = (A0 % 8) ^ 2 ^ 7 ^ (A0 // 2**((A0 % 8) ^ 2))
#   12: out = (A0 % 8) ^ 2 ^ 7 ^ (A0 // 2**((A0 % 8) ^ 2)) % 8
#
# And we see A is divided by 8 after each iteration.
#
# Since A is zero when the program terminates, it must be some value 1 through 7
# when the output number is outputted (in my case 0). So try running the
# computer with all values and see if you get 0 for output. For any A values
# where you did get an output value 0, try appending to A (in octal) all
# possible values 0-7 and run the computer with A equal to those two octal
# digits, seeing which of those A values cause the correct last two output
# digits to be printed. Repeat this process for every output digit, so that you
# are building up A by iterating over the output digits in reverse. There can
# sometimes be more than one octet we could append to A which would give the
# correct output so far, in which case we need to recursively search both
# possible options (starting with the lower value since we want the lowest
# possible A value that works).

def A_to_out(a: int) -> list[int]:
    """
    Returns the output from the  computer when initialized with a given A
    register value.
    """

    p2_computer = Computer(a, B, C)
    p2_computer.execute(program)
    return p2_computer.output

def try_find_p2(a: int, program: list[int]) -> tuple[bool, int]:
    if len(program) == 0:
        return (True, a)

    octet = program[-1]
    a *= 8

    for i in range(8):
        try_a  = a + i
        out = A_to_out(try_a)[0]
        if out == octet:
            found, ret = try_find_p2(try_a, program[:-1])
            if found:
                return (True, ret)

    return False, -1

print(program)
found, p2_answer = try_find_p2(0, program)
print(f"found: {found}")
print(A_to_out(p2_answer))
print(f"p2 answer: {p2_answer}")
