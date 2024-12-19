from functools import cache


def part1(input_file):
    patterns, designs = load_data(input_file)

    @cache
    def design_is_possible(design):
        if design == "":
            return True
        max_pattern_len = max(map(len, patterns))
        for i in range(min(len(design), max_pattern_len) + 1):
            if design[:i] in patterns and design_is_possible(design[i:]):
                return True
        return False

    possible = [design for design in designs if design_is_possible(design)]
    return len(possible)


def part2(input_file):
    patterns, designs = load_data(input_file)

    @cache
    def design_counter(design):
        total = 0
        if design == "":
            return 1
        max_pattern_len = max(map(len, patterns))
        for i in range(min(len(design), max_pattern_len) + 1):
            if design[:i] in patterns:
                total += design_counter(design[i:])
        return total

    return sum([design_counter(design) for design in designs])


def load_data(input_file):
    with open(input_file) as f:
        raw_patterns, raw_designs = f.read().split("\n\n")
    patterns = raw_patterns.split(", ")
    designs = raw_designs.split("\n")
    return patterns, designs
