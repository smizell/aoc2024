import operator

ops = {"add": operator.add, "mul": operator.mul, "concat": lambda a, b: int(f"{a}{b}")}


def part1(input_file):
    equations = load_equations(input_file)
    true_equations = []
    for total, numbers in equations:
        if solve1(total, numbers):
            true_equations.append(total)
    return sum(true_equations)


# 6042069247243 is too low
def part2(input_file):
    equations = load_equations(input_file)
    true_equations = []
    for total, numbers in equations:
        if solve2(total, numbers):
            true_equations.append(total)
    return sum(true_equations)


def solve1(fin_total, numbers, cur_total=0):
    if not numbers:
        return False
    number, *rest_numbers = numbers
    ops = [operator.add, operator.mul]
    for op in ops:
        new_total = op(cur_total, number)
        if not rest_numbers and new_total == fin_total:
            return True
        if solve1(fin_total, rest_numbers, new_total):
            return True
    return False


def solve2(fin_total, numbers, cur_total=0):
    if not numbers:
        return False
    number, *rest_numbers = numbers
    ops = [operator.add, operator.mul, lambda a, b: int(f"{a}{b}")]
    for op in ops:
        new_total = op(cur_total, number)
        if not rest_numbers and new_total == fin_total:
            return True
        if solve2(fin_total, rest_numbers, new_total):
            return True
    return False


def load_equations(input_file):
    with open(input_file) as f:
        raw_data = [
            [parts for parts in line.split(": ")] for line in f.read().split("\n")
        ]
        return [
            [
                int(string_total),
                [int(string_number) for string_number in string_numbers.split(" ")],
            ]
            for string_total, string_numbers in raw_data
        ]
