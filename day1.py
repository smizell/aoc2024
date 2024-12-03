import collections


def part1(input_file):
    loc1, loc2 = load_data(input_file)
    distances = [abs(col1 - col2) for col1, col2 in zip(loc1, loc2)]
    return sum(distances)


def part2(input_file):
    loc1, loc2 = load_data(input_file)
    counts = collections.Counter(loc2)
    similarity_score = [num * counts[num] for num in loc1]
    return sum(similarity_score)


def load_data(input_file):
    with open(input_file) as f:
        raw_data = f.read()

    return [
        sorted(locations)
        for locations in zip(
            *[
                [int(column) for column in row.split("   ")]
                for row in raw_data.split("\n")
            ]
        )
    ]
