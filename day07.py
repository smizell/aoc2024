import operator


def part1(input_file):
    equations = load_equations(input_file)
    true_equations = []
    for total, numbers in equations:
        if solve(total, numbers):
            true_equations.append(total)
    return sum(true_equations)


def solve(fin_total, numbers, cur_total=0):
    if not numbers:
        return False
    number, *rest_numbers = numbers
    ops = [operator.add, operator.mul]
    for op in ops:
        new_total = op(cur_total, number)
        if not rest_numbers and new_total == fin_total:
            return True
        if solve(fin_total, rest_numbers, new_total):
            return True


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
