import re
from collections import namedtuple
from functools import reduce
from operator import mul

Coor = namedtuple("Coor", ["x", "y"])


def part1(input_file):
    robots = load_robots(input_file)
    space = get_space(input_file)
    seconds = 100
    robots = move_robots(robots, space, seconds)
    grouped_robots = group_in_quadrants(robots, space)
    return reduce(mul, map(len, grouped_robots))


def part2(input_file):
    robots = load_robots(input_file)
    space = get_space(input_file)
    seconds = find_tree(list(robots), space)
    return seconds


def find_tree(robots, space):
    while True:
        robots = tick_robots(robots, space)
        print(render_robots(robots, space))
        input()


def tick_robots(robots, space):
    return move_robots(robots, space, 1)


def render_robots(robots, space):
    robot_poss = set([pos for pos, _ in robots])
    txt = ""
    for y in range(space.y):
        for x in range(space.x):
            if Coor(x, y) in robot_poss:
                txt += "X"
            else:
                txt += " "
        txt += "\n"
    return txt


def move_robots(robots, space, seconds):
    new_robots = []
    for robot in robots:
        pos, vel = robot
        diff = Coor(vel.x * seconds, vel.y * seconds)
        new_pos = Coor(pos.x + diff.x, pos.y + diff.y)
        collected = Coor(new_pos.x % (space.x + 1), new_pos.y % (space.y + 1))
        new_robots.append((collected, vel))
    return new_robots


def group_in_quadrants(robots, space):
    grouped_robots = []
    quadrants = get_quadrants(space)
    for start, end in quadrants:
        robots_in_quadrants = []
        for pos, _ in robots:
            if end.x >= pos.x >= start.x and end.y >= pos.y >= start.y:
                robots_in_quadrants.append(pos)
        grouped_robots.append(robots_in_quadrants)
    return [group for group in grouped_robots if len(group) > 0]


def get_quadrants(space):
    middle = get_middle(space)
    return [
        [Coor(0, 0), Coor(middle.x - 1, middle.y - 1)],
        [Coor(middle.x + 1, 0), Coor(space.x, middle.y - 1)],
        [Coor(0, middle.y + 1), Coor(middle.x - 1, space.y)],
        [Coor(middle.x + 1, middle.y + 1), Coor(space.x, space.y)],
    ]


def get_middle(space):
    return Coor(int((space.x - 1) / 2) + 1, int((space.y - 1) / 2) + 1)


robot_re = r"p=(-?\d*),(-?\d*) v=(-?\d*),(-?\d*)"


def load_robots(input_file):
    with open(input_file) as f:
        raw_robots = f.read().split("\n")
        for raw_robot in raw_robots:
            px, py, vx, vy = list(map(int, re.findall(robot_re, raw_robot)[0]))
            yield Coor(px, py), Coor(vx, vy)


def get_space(input_file):
    if "example" in input_file:
        return Coor(10, 6)
    return Coor(100, 102)
