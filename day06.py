from copy import deepcopy
from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Visible(Enum):
    OBSTACLE = "obstacle"
    EMPTY = "empty"
    EDGE = "edge"


def part1(input_file):
    grid = load_grid(input_file)
    guard_path = find_guard_path(grid)
    return len(set(guard_path))


def find_guard_path(grid):
    guard_position = find_guard(grid)
    guard_direction = Direction.UP
    guard_path = []
    while within_grid(grid, guard_position):
        guard_path.append(guard_position)
        guard_position, guard_direction = move_guard(
            grid, guard_position, guard_direction
        )
    return guard_path


def part2(input_file):
    original_grid = load_grid(input_file)
    loop_grids = potential_loop_grids(original_grid)
    found_loop_grids = []
    for grid in loop_grids:
        guard_position = find_guard(grid)
        guard_direction = Direction.UP
        guard_visited = {
            (x, y): 0 for y in range(len(grid)) for x in range(len(grid[0]))
        }
        while within_grid(grid, guard_position):
            guard_visited[guard_position] += 1
            # There are 4 directions the guard can go, which means the guard
            # could cross the same position 4 times and not bein a loop.
            if guard_visited[guard_position] > 4:
                found_loop_grids.append(grid)
                break
            guard_position, guard_direction = move_guard(
                grid, guard_position, guard_direction
            )
    return len(found_loop_grids)


def move_guard(grid, guard_position, guard_direction):
    if guard_sees_obstacle(grid, guard_position, guard_direction):
        return guard_position, turn_right(guard_direction)
    else:
        return move_forward(grid, guard_position, guard_direction), guard_direction


def load_grid(input_file):
    with open(input_file) as f:
        return [list(row) for row in f.read().split("\n")]


def find_guard(grid):
    for row_idx, columns in enumerate(grid):
        for column_idx, value in enumerate(columns):
            if value == "^":
                return (column_idx, row_idx)


def within_grid(grid, position):
    return len(grid[0]) > position[0] >= 0 and len(grid) > position[1] >= 0


def guard_sees_obstacle(grid, guard_position, guard_direction):
    next_position = get_next_position(grid, guard_position, guard_direction)
    what_guard_sees = get_from_grid(grid, next_position)
    return what_guard_sees == Visible.OBSTACLE


def get_next_position(grid, position, direction):
    match direction:
        case Direction.UP:
            return (position[0], position[1] - 1)
        case Direction.DOWN:
            return (position[0], position[1] + 1)
        case Direction.LEFT:
            return (position[0] - 1, position[1])
        case Direction.RIGHT:
            return (position[0] + 1, position[1])


def get_from_grid(grid, position):
    if not within_grid(grid, position):
        return Visible.EDGE
    value = grid[position[1]][position[0]]
    match value:
        case "." | "^":
            return Visible.EMPTY
        case "#":
            return Visible.OBSTACLE


def turn_right(direction):
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP
        case Direction.RIGHT:
            return Direction.DOWN


def move_forward(grid, position, direction):
    return get_next_position(grid, position, direction)


def add_obstacle_to_grid(grid, position):
    grid[position[1]][position[0]] = "#"


def potential_loop_grids(grid):
    possible_obstacales = set(find_guard_path(grid)[1:])
    guard_position = find_guard(grid)
    grids = []
    for change_position in possible_obstacales:
        visible = get_from_grid(grid, change_position)
        if visible == Visible.OBSTACLE or change_position == guard_position:
            continue
        new_grid = deepcopy(grid)
        add_obstacle_to_grid(new_grid, change_position)
        grids.append(new_grid)
    return grids
