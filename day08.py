import itertools


def part1(input_file):
    ant_map = load_map(input_file)
    return len(find_antinodes1(ant_map))


def part2(input_file):
    ant_map = load_map(input_file)
    return len(find_antinodes2(ant_map))


def find_ants(ant_map):
    for y, row in enumerate(ant_map):
        for x, value in enumerate(row):
            if value == ".":
                continue
            yield (x, y), value


def find_antinodes1(ant_map):
    all_antinodes = set()
    value_map = create_value_map(ant_map)
    # We go through each combination of coordinates for a given value
    # We then find the slope, find the possible antinodes, and decide
    # if those antinodes are on the map. If so, we capture it in set.
    for coors in value_map.values():
        for coor_a, coor_b in itertools.combinations(coors, 2):
            slope = find_slope(coor_a, coor_b)
            antinode_a = coor_a[0] - slope[0], coor_a[1] - slope[1]
            antinode_b = coor_b[0] + slope[0], coor_b[1] + slope[1]
            antinodes = [antinode_a, antinode_b]
            for antinode in antinodes:
                if within_ant_map(ant_map, antinode):
                    all_antinodes.add(antinode)
    return list(all_antinodes)


def find_antinodes2(ant_map):
    all_antinodes = set()
    value_map = create_value_map(ant_map)
    for coors in value_map.values():
        for coor_a, coor_b in itertools.combinations(coors, 2):
            slope = find_slope(coor_a, coor_b)
            # Follow coor_a in the negative
            curr_coor_a = coor_a
            while within_ant_map(ant_map, curr_coor_a):
                all_antinodes.add(curr_coor_a)
                curr_coor_a = curr_coor_a[0] - slope[0], curr_coor_a[1] - slope[1]
            # Follow coor_a in the positive
            curr_coor_b = coor_b
            while within_ant_map(ant_map, curr_coor_b):
                all_antinodes.add(curr_coor_b)
                curr_coor_b = curr_coor_b[0] + slope[0], curr_coor_b[1] + slope[1]
    return list(all_antinodes)


def create_value_map(ant_map):
    value_map = {}
    for coor, value in find_ants(ant_map):
        if value not in value_map:
            value_map[value] = []
        value_map[value].append(coor)
    return value_map


def find_slope(coor_a, coor_b):
    return coor_b[0] - coor_a[0], coor_b[1] - coor_a[1]


# Assumes the coor is within the map
def get_from_map(ant_map, coor):
    return ant_map[coor[1]][coor[0]]


def within_ant_map(ant_map, coor):
    return len(ant_map[0]) > coor[0] >= 0 and len(ant_map) > coor[1] >= 0


def load_map(input_file):
    with open(input_file) as f:
        return [list(row) for row in f.read().split("\n")]
