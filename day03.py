import re


def load_memory_dump(input_file):
    with open(input_file) as f:
        return f.read()


def process_instructions(instructions):
    findings = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", instructions)
    args = [[int(number) for number in numbers] for numbers in findings]
    results = sum([arg[0] * arg[1] for arg in args])
    return results


def part1(input_file):
    memory_dump = load_memory_dump(input_file)
    results = process_instructions(memory_dump)
    return results


def part2(input_file):
    memory_dump = load_memory_dump(input_file)
    instructions = [dos.split("don't()")[0] for dos in memory_dump.split("do()")]
    results = sum([process_instructions(instruction) for instruction in instructions])
    return results
