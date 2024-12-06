def part1(input_file):
    reports = load_data(input_file)
    return len([level for level in reports if is_safe_level(level)])


def part2(input_file):
    reports = load_data(input_file)
    return len([level for level in reports if is_safe_with_dampener(level)])


def load_data(input_file):
    with open(input_file) as f:
        raw_data = f.read()

    return [[int(level) for level in report.split()] for report in raw_data.split("\n")]


def is_safe_level(level):
    direction = None
    for i in range(0, len(level) - 1):
        num1 = level[i]
        num2 = level[i + 1]
        if direction is None:
            if num1 > num2:
                direction = "desc"
            if num1 < num2:
                direction = "asc"
        if not is_safe_step(direction, num1, num2):
            return False
    return True


def is_safe_with_dampener(level):
    if is_safe_level(level):
        return True
    for i in range(0, len(level)):
        level_copy = level.copy()
        del level_copy[i]
        if is_safe_level(level_copy):
            return True
    return False


def is_safe_step(direction, num1, num2):
    if num1 > num2 and direction == "asc":
        return False
    elif num2 > num1 and direction == "desc":
        return False
    elif num1 == num2:
        return False
    difference = abs(num1 - num2)
    if difference < 1 or difference > 3:
        return False

    return True
