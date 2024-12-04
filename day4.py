from itertools import chain


def part1(input_file):
    puzzle = load_puzzle(input_file)
    coordinates = [(x, y) for x in range(len(puzzle[0])) for y in range(len(puzzle))]
    possible_coordinates = [
        [
            [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)],
            [(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)],
            [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)],
            [(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)],
            [(x, y), (x - 1, y), (x - 2, y), (x - 3, y)],
            [(x, y), (x - 1, y - 1), (x - 2, y - 2), (x - 3, y - 3)],
            [(x, y), (x, y - 1), (x, y - 2), (x, y - 3)],
            [(x, y), (x + 1, y - 1), (x + 2, y - 2), (x + 3, y - 3)],
        ]
        for x, y in coordinates
    ]
    return find_word(puzzle, chain(*possible_coordinates), "XMAS")


def part2(input_file):
    puzzle = load_puzzle(input_file)
    coordinates = [(x, y) for x in range(len(puzzle[0])) for y in range(len(puzzle))]
    # I'm sure there's a better way to do this.
    # I made up the pattern AMSMS and looked for that based on the coordinates
    # that would match it. I'm guessing you could do some product of some lists.
    possible_coordinates = [
        [
            [(x, y), (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1)],
            [(x, y), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)],
            [(x, y), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)],
            [(x, y), (x - 1, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1)],
        ]
        for x, y in coordinates
    ]
    return find_word(puzzle, chain(*possible_coordinates), "AMSMS")


def find_word(puzzle, possible_coordinates, expected_word):
    word_count = 0
    for coordinates in possible_coordinates:
        try:
            found_word = "".join(
                [puzzle[y][x] for x, y in coordinates if x >= 0 and y >= 0]
            )
            if found_word == expected_word:
                word_count += 1
        except IndexError:
            continue
    return word_count


def load_puzzle(input_file):
    with open(input_file) as f:
        return [list(row) for row in f.read().strip().split("\n")]
