def part1(input_file):
    track, start, end = load_track(input_file)
    track_distances = get_track_distances(track, start, end)
    cheats = find_cheats(track, track_distances, start, end)
    return len([cheat for cheat in cheats if cheat[1] >= 100])


def build_report(cheats):
    report = {}
    for _, distance in cheats:
        if distance not in report:
            report[distance] = 0
        report[distance] += 1
    return report


def get_track_distances(track, start, end):
    distances = {}
    distances[start] = 0
    curr_pos = start
    while True:
        next_pos = find_next_pos(track, distances, curr_pos)
        distances[next_pos] = distances[curr_pos] + 1
        if next_pos == end:
            break
        curr_pos = next_pos
    return distances


def find_next_pos(track, distances, pos):
    for adj_pos in get_adj_poss(track, pos):
        if adj_pos in distances:
            continue
        if adj_pos in track:
            return adj_pos


adj_diffs = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def get_adj_poss(track, pos):
    adj_poss = [(pos[0] + diff[0], pos[1] + diff[1]) for diff in adj_diffs]
    return [adj_pos for adj_pos in adj_poss if adj_pos in track]


def find_cheats(track, distances, start, end):
    cheats = []
    for pos in track:
        possible_cheats = get_possible_cheats(track, pos)
        for possible_cheat in possible_cheats:
            distance = distances[possible_cheat] - distances[pos]
            if distance > 2:
                cheats.append((possible_cheat, distance - 2))
    return cheats


adj_cheat_diffs = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
    (1, 1),
    (2, 0),
    (0, -2),
    (-2, 0),
    (0, 2),
]


def get_possible_cheats(track, pos):
    possible_cheats = []
    for diff in adj_cheat_diffs:
        possible_pos = pos[0] + diff[0], pos[1] + diff[1]
        if possible_pos in track:
            possible_cheats.append(possible_pos)
    return possible_cheats


def load_track(input_file):
    with open(input_file) as f:
        rows = f.read().split("\n")
    start = None
    end = None
    track = []
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            match value:
                case "S":
                    start = (x, y)
                    track.append((x, y))
                case "E":
                    end = (x, y)
                    track.append((x, y))
                case ".":
                    track.append((x, y))
    return track, start, end
