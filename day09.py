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


def part2(input_file):
    raw_disk_map = load_disk_map(input_file)
    disk_map = build_disk_map(raw_disk_map)
    defragged = defrag2(list(disk_map))
    representation = build_representation(defragged)
    checksum = sum(
        [
            idx * int(value)
            for idx, value in enumerate(representation)
            if str(value) != "."
        ]
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


def disk_map_to_string(disk_map):
    return "".join(build_representation(disk_map))


def defrag1(disk_map):
    while True:
        free_idx, _ = find_first_free_space(disk_map)
        last_file_idx, _ = find_last_file(disk_map)
        if last_file_idx <= free_idx:
            break
        disk_map[free_idx] = disk_map[last_file_idx]
        disk_map[last_file_idx] = "."
    return disk_map


def defrag2(disk_map):
    for file_idx, file_block in reverse_files(disk_map):
        # print(disk_map_to_string(disk_map))
        free_idx, free_block = find_first_free_space_by_size(
            disk_map, file_block.size()
        )
        if not free_idx:
            continue
        if file_idx < free_idx:
            continue
        disk_map[free_idx] = file_block
        disk_map[file_idx] = FreeSpace(file_block.size())
        if free_block.size() > file_block.size():
            disk_map.insert(
                free_idx + 1, FreeSpace(free_block.size() - file_block.size())
            )
    return disk_map


def find_first_free_space(disk_map):
    return next(find_free_space(disk_map))


def find_free_space(disk_map):
    for idx, block in enumerate(disk_map):
        if str(block) == ".":
            yield idx, block


def find_first_free_space_by_size(disk_map, size):
    for idx, free_block in find_free_space(disk_map):
        if free_block.size() >= size:
            return idx, free_block
    return None, None


def find_last_file(disk_map):
    return next(reverse_files(disk_map))


def find_last_file_with_size(disk_map, size):
    for idx, file_block in reverse_files(disk_map):
        if file_block.size() <= size:
            return idx, file_block


def reallocate_free_blocks(disk_map):
    new_disk_map = []
    curr_free_blocks = []
    for block in disk_map:
        if block is not FreeSpace:
            if curr_free_blocks:
                combined_sizes = sum(
                    [free_block.size() for free_block in curr_free_blocks]
                )
                new_disk_map.append(FreeSpace(combined_sizes))
                curr_free_blocks = []
            new_disk_map.append(block)
        else:
            curr_free_blocks.append(block)
    return new_disk_map


def reverse_files(disk_map):
    max_id = len(disk_map) - 1
    for idx in range(len(disk_map)):
        value_idx = max_id - idx
        if str(disk_map[value_idx]) != ".":
            yield value_idx, disk_map[value_idx]


@dataclass
class File:
    id: int
    blocks: int

    def __str__(self):
        return str(self.id)

    def size(self):
        return self.blocks


@dataclass
class FreeSpace:
    blocks: int

    def __str__(self):
        return "."

    def size(self):
        return self.blocks


def load_disk_map(input_file):
    with open(input_file) as f:
        return [int(value) for value in list(f.read())]
