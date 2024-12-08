import itertools


def part1(input_file):
    ant_map = load_map(input_file)
    return len(find_antinodes(ant_map))


def find_ants(ant_map):
    for y, row in enumerate(ant_map):
        for x, value in enumerate(row):
            if value == ".":
                continue
            yield (x, y), value


def find_antinodes(ant_map):
    all_antinodes = set()
    # This maps all node values to every matching coordinate
    value_map = {}
    for coor, value in find_ants(ant_map):
        if value not in value_map:
            value_map[value] = []
        value_map[value].append(coor)
    # We go through each combination of coordinates for a given value
    # We then find the slope, find the possible antinodes, and decide
    # if those antinodes are on the map. If so, we capture it in set.
    for value, coors in value_map.items():
        for coor_a, coor_b in itertools.combinations(coors, 2):
            slope = coor_b[0] - coor_a[0], coor_b[1] - coor_a[1]
            antinode_a = coor_a[0] - slope[0], coor_a[1] - slope[1]
            antinode_b = coor_b[0] + slope[0], coor_b[1] + slope[1]
            antinodes = [antinode_a, antinode_b]
            for antinode in antinodes:
                if within_ant_map(ant_map, antinode):
                    all_antinodes.add(antinode)
    return list(all_antinodes)


# Assumes the coor is within the map
def get_from_map(ant_map, coor):
    return ant_map[coor[1]][coor[0]]


def within_ant_map(ant_map, coor):
    return len(ant_map[0]) > coor[0] >= 0 and len(ant_map) > coor[1] >= 0


def load_map(input_file):
    with open(input_file) as f:
        return [list(row) for row in f.read().split("\n")]
