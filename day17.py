# 1,4,7,6,7,0,7,7,5 wrong
def part1(input_file):
    a, b, c, program = load_program(input_file)
    out = []
    ptr = 0

    def combo(operand):
        if 3 >= operand >= 0:
            return operand
        if operand == 4:
            return a
        if operand == 5:
            return b
        if operand == 6:
            return c
        raise "Critical error"

    while True:
        if ptr >= len(program):
            break
        opcode = program[ptr]
        operand = program[ptr + 1]
        if opcode == 0:
            a = int(a / pow(2, combo(operand)))
        elif opcode == 1:
            b = b ^ operand
        elif opcode == 2:
            b = combo(operand) % 8
        elif opcode == 3:
            if a != 0:
                ptr = operand
                continue
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            out.append(combo(operand) % 8)
        elif opcode == 6:
            b = int(a / pow(2, combo(operand)))
        elif opcode == 7:
            c = int(a / pow(2, combo(operand)))
        ptr += 2

    return ",".join(map(str, out))


def load_program(input_file):
    with open(input_file) as f:
        raw_registers, raw_program = f.read().split("\n\n")
        raw_registers = raw_registers.split("\n")
    reg_a = int(raw_registers[0].split(": ")[1])
    reg_b = int(raw_registers[1].split(": ")[1])
    reg_c = int(raw_registers[2].split(": ")[1])
    program = [int(num_str) for num_str in raw_program.split(": ")[1].split(",")]
    return reg_a, reg_b, reg_c, program
