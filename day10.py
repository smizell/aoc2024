def part1(input_file):
    hiking_map = load_hiking_map(input_file)
    trailheads = find_trailheads(hiking_map)
    total_paths = [
        len(set(find_total_paths(hiking_map, trailhead))) for trailhead in trailheads
    ]
    return sum(total_paths)


def part2(input_file):
    hiking_map = load_hiking_map(input_file)
    trailheads = find_trailheads(hiking_map)
    total_paths = [
        len(find_total_paths(hiking_map, trailhead)) for trailhead in trailheads
    ]
    return sum(total_paths)


def find_trailheads(hiking_map):
    for y, row in enumerate(hiking_map):
        for x, height in enumerate(row):
            if height == 0:
                yield x, y


def find_total_paths(hiking_map, pos):
    height = get_from_map(hiking_map, pos)
    if height == 9:
        return [pos]
    total_paths = []
    for step in next_steps(hiking_map, pos, height):
        total_paths += find_total_paths(hiking_map, step)
    return total_paths


adjacent_diffs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def next_steps(hiking_map, pos, height):
    visible_steps = find_visible_steps(hiking_map, pos)
    for step in visible_steps:
        next_height = get_from_map(hiking_map, step)
        if next_height != "." and next_height == height + 1:
            yield step


def find_visible_steps(hiking_map, pos):
    for diff in adjacent_diffs:
        possible_pos = pos[0] + diff[0], pos[1] + diff[1]
        if within_hiking_map(hiking_map, possible_pos):
            yield possible_pos


def get_from_map(hiking_map, pos):
    return hiking_map[pos[1]][pos[0]]


def within_hiking_map(hiking, pos):
    return len(hiking[0]) > pos[0] >= 0 and len(hiking) > pos[1] >= 0


def load_hiking_map(input_file):
    with open(input_file) as f:
        return [[int(column) for column in row] for row in f.read().split("\n")]
