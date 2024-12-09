from dataclasses import dataclass


def part1(input_file):
    raw_disk_map = load_disk_map(input_file)
    disk_map = build_disk_map(raw_disk_map)
    representation = build_representation(disk_map)
    defragged = defrag1(representation)
    checksum = sum(
        [idx * int(value) for idx, value in enumerate(defragged) if value != "."]
    )
    return checksum


def build_disk_map(raw_disk_map):
    curr_id = 0
    for idx, blocks in enumerate(raw_disk_map):
        if idx % 2 == 0:
            yield File(curr_id, blocks)
            curr_id += 1
        else:
            yield FreeSpace(blocks)


def build_representation(disk_map):
    representation = []
    for item in disk_map:
        for _ in range(item.blocks):
            representation.append(str(item))
    return representation


def defrag1(disk_map):
    free_idx, _ = find_first_free_space(disk_map)
    last_file_finder = find_last_file_idx(disk_map)
    last_file_idx, _ = next(last_file_finder)
    while free_idx <= last_file_idx:
        disk_map[free_idx] = disk_map[last_file_idx]
        disk_map[last_file_idx] = "."
        free_idx, _ = find_first_free_space(disk_map)
        last_file_idx, _ = next(last_file_finder)
    return disk_map


def find_first_free_space(representation):
    for idx, block in enumerate(representation):
        if str(block) == ".":
            return idx, block


def find_last_file_idx(representation):
    max_id = len(representation) - 1
    for idx in range(len(representation)):
        value_idx = max_id - idx
        if str(representation[value_idx]) != ".":
            yield value_idx, representation[value_idx]


@dataclass
class File:
    id: int
    blocks: int

    def __str__(self):
        return str(self.id)

    def length(self):
        return self.blocks


@dataclass
class FreeSpace:
    blocks: int

    def __str__(self):
        return "."

    def length(self):
        return self.blocks


def load_disk_map(input_file):
    with open(input_file) as f:
        return [int(value) for value in list(f.read())]
