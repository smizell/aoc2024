from functools import cache

numeric_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]

numeric_keypad_start = (2, 3)

dir_keypad = [
    [None, "^", "A"],
    ["<", "v", ">"],
]

dir_keypad_start = (2, 0)

dir_diffs = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


# 137136 is too high
def part1(input_file):
    codes = load_codes(input_file)
    sequences = list(map(get_sequence, codes))
    code_nums = [int(code[:-1]) for code in codes]
    return sum(
        [len(sequence) * code_num for sequence, code_num in zip(sequences, code_nums)]
    )


def operate_sequence(sequence):
    dir2 = operate_dir_keypad(sequence)
    dir1 = operate_dir_keypad(dir2)
    return operate_numeric_keypad(dir1)


def get_sequence(value):
    numeric_commands = get_numeric_commands(value)
    dir_commands1 = get_dir_commands(numeric_commands)
    dir_commands2 = get_dir_commands(dir_commands1)
    return dir_commands2


def get_numeric_commands(values):
    values = list(values)
    curr_pos = numeric_keypad_start
    commands = ""
    for value in values:
        curr_value = get_from_keypad(numeric_keypad, curr_pos)
        value_pos = get_numeric_pos(value)
        diff = get_diff(value_pos, curr_pos)
        commands += commands_from_diff(diff, curr_value)
        commands += "A"
        curr_pos = value_pos
    return commands


def get_dir_commands(values):
    values = list(values)
    curr_pos = dir_keypad_start
    commands = ""
    for value in values:
        curr_value = get_from_keypad(dir_keypad, curr_pos)
        value_pos = get_dir_pos(value)
        diff = get_diff(value_pos, curr_pos)
        commands += commands_from_diff(diff, curr_value)
        commands += "A"
        curr_pos = value_pos
    return commands


def get_diff(pos1, pos2):
    return pos1[0] - pos2[0], pos1[1] - pos2[1]


def commands_from_diff(diff, value):
    commands = ""
    dirs = get_preferred_order(value)
    for dir in dirs:
        if dir == "x":
            if diff[0] < 0:
                commands += "<" * abs(diff[0])
            else:
                commands += ">" * abs(diff[0])
        elif dir == "y":
            if diff[1] < 0:
                commands += "^" * abs(diff[1])
            else:
                commands += "v" * abs(diff[1])
    return commands


# Just making sure we don't go into the gap
def get_preferred_order(value):
    if value in [0, "A", "^"]:
        return ("y", "x")
    return ("x", "y")


@cache
def get_numeric_pos(value):
    for y, row in enumerate(numeric_keypad):
        for x, keypad_value in enumerate(row):
            if keypad_value == value:
                return (x, y)


@cache
def get_dir_pos(value):
    for y, row in enumerate(dir_keypad):
        for x, keypad_value in enumerate(row):
            if keypad_value == value:
                return (x, y)


def operate_numeric_keypad(commands):
    curr_pos = numeric_keypad_start
    result = ""
    for command in commands:
        if get_from_keypad(numeric_keypad, curr_pos) is None:
            raise Exception("Oh no! Num error.", curr_pos)
        if command == "A":
            result += str(get_from_keypad(numeric_keypad, curr_pos))
        else:
            diff = dir_diffs[command]
            curr_pos = curr_pos[0] + diff[0], curr_pos[1] + diff[1]
    return result


def operate_dir_keypad(commands):
    curr_pos = dir_keypad_start
    result = ""
    for command in commands:
        if get_from_keypad(dir_keypad, curr_pos) is None:
            raise Exception("Oh no! Dir error.", curr_pos)
        if command == "A":
            result += str(get_from_keypad(dir_keypad, curr_pos))
        else:
            diff = dir_diffs[command]
            curr_pos = curr_pos[0] + diff[0], curr_pos[1] + diff[1]
    return result


def get_from_keypad(keypad, pos):
    return keypad[pos[1]][pos[0]]


def load_codes(input_file):
    with open(input_file) as f:
        return f.read().split("\n")
