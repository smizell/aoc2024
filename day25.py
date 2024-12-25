def part1(input_file):
    locks, keys = load_data(input_file)
    unique_pairs = []
    for lock in locks:
        for key in keys:
            if is_match(lock, key):
                unique_pairs.append((lock, key))
    return len(unique_pairs)


def is_match(lock, key):
    for lh, kh in zip(lock, key):
        if (lh + kh) > 5:
            return False
    return True


def load_data(input_file):
    locks, keys = [], []
    with open(input_file) as f:
        items = [row.split("\n") for row in f.read().split("\n\n")]
    for item in items:
        heights = [-1, -1, -1, -1, -1]
        for row in item:
            for idx, column in enumerate(row):
                if column == "#":
                    heights[idx] += 1
        if item[0][0] == "#":
            locks.append(heights)
        else:
            keys.append(heights)
    return locks, keys
