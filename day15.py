from dataclasses import dataclass


@dataclass
class Warehouse:
    walls: set
    boxes: set
    robot: tuple


diffs = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


def part1(input_file):
    warehouse, moves = load_data1(input_file)
    warehouse = operate_robot1(warehouse, moves)
    display_warehouse1(warehouse)
    sum_of_coors = calc_sum_of_coors1(warehouse)
    return sum_of_coors


def operate_robot1(warehouse, moves):
    for move in moves:
        first_empty = find_first_empty1(warehouse, move)
        if not first_empty:
            continue
        warehouse.robot = move_item1(warehouse.robot, move)
        if warehouse.robot in warehouse.boxes:
            warehouse.boxes.remove(warehouse.robot)
            warehouse.boxes.add(first_empty)
    return warehouse


def move_item1(item, move):
    diff = diffs[move]
    return item[0] + diff[0], item[1] + diff[1]


def find_first_empty1(warehouse, move):
    curr_loc = warehouse.robot
    while True:
        curr_loc = move_item1(curr_loc, move)
        if curr_loc in warehouse.walls:
            return None
        if curr_loc not in warehouse.boxes:
            return curr_loc


def calc_sum_of_coors1(warehouse):
    total = 0
    for box in warehouse.boxes:
        total += (box[1] * 100) + box[0]
    return total


def display_warehouse1(warehouse):
    txt = ""
    warehouse
    width, height = (
        max([wall[0] for wall in warehouse.walls]) + 1,
        max([wall[1] for wall in warehouse.walls]) + 1,
    )
    for y in range(height):
        for x in range(width):
            if (x, y) in warehouse.walls:
                txt += "#"
            elif (x, y) in warehouse.boxes:
                txt += "O"
            elif warehouse.robot == (x, y):
                txt += "@"
            else:
                txt += "."
        txt += "\n"
    print(txt)


def load_data1(input_file):
    with open(input_file) as f:
        raw_warehouse, raw_moves = f.read().split("\n\n")
    warehouse = parse_warehouse1(raw_warehouse)
    moves = list(raw_moves.replace("\n", ""))
    return warehouse, moves


def parse_warehouse1(raw_warehouse):
    warehouse = Warehouse(set(), set(), ())
    for y, row in enumerate(raw_warehouse.split("\n")):
        for x, value in enumerate(list(row)):
            match value:
                case "#":
                    warehouse.walls.add((x, y))
                case "O":
                    warehouse.boxes.add((x, y))
                case "@":
                    warehouse.robot = (x, y)
                case _:
                    None
    return warehouse
