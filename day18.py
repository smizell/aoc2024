from collections import deque

adj_diffs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def part1(input_file):
    bytes = get_bytes(input_file)
    corrupted = load_corrupted(input_file)
    dimensions = get_grid_dimensions(input_file)
    return find_shortest_path(bytes, corrupted, dimensions)


def part2(input_file):
    corrupted = load_corrupted(input_file)
    # Start at the end
    bytes = len(corrupted) - 1
    dimensions = get_grid_dimensions(input_file)
    while True:
        bytes -= 1
        if find_shortest_path(bytes, corrupted, dimensions):
            coor = corrupted[bytes]
            return f"{coor[0]},{coor[1]}"


def find_shortest_path(bytes, corrupted, dimensions):
    corrupted = corrupted[0:bytes]
    distances = {
        (x, y): -1 for x in range(dimensions[0] + 1) for y in range(dimensions[1] + 1)
    }
    distances[(0, 0)] = 0
    queue = deque()
    queue.append((0, 0))
    while queue:
        pos = queue.popleft()
        adj_poss = find_adj_memory(dimensions, pos)
        for adj_pos in adj_poss:
            if distances[adj_pos] != -1:
                continue
            if adj_pos not in corrupted:
                distances[adj_pos] = distances[pos] + 1
                queue.append(adj_pos)
    if distances[dimensions] == -1:
        return None
    return distances[dimensions]


def render_grid(dimensions, corrupted, distances={}):
    txt = ""
    for y in range(dimensions[0] + 1):
        for x in range(dimensions[1] + 1):
            if (x, y) in corrupted:
                txt += "#"
            else:
                if (x, y) in distances:
                    txt += str(distances[(x, y)])
                else:
                    txt += "."
        txt += "\n"
    return txt


def within_memory(dimensions, pos):
    return dimensions[0] >= pos[0] >= 0 and dimensions[1] >= pos[1] >= 0


def find_adj_memory(dimensions, curr_pos):
    poss = []
    for diff in adj_diffs:
        pos = curr_pos[0] + diff[0], curr_pos[1] + diff[1]
        if within_memory(dimensions, pos):
            poss.append(pos)
    return poss


def get_grid_dimensions(input_file):
    if "example" in input_file:
        return (6, 6)
    return (70, 70)


def get_bytes(input_file):
    if "example" in input_file:
        return 12
    return 1024


def load_corrupted(input_file):
    with open(input_file) as f:
        rows = [row.split(",") for row in f.read().split("\n")]
        return [(int(row[0]), int(row[1])) for row in rows]
