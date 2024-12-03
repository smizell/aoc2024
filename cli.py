#!/usr/bin/env python3

import sys


def get_part_method(day, part):
    module = __import__(f"day{day}")
    return getattr(module, f"part{part}")


match sys.argv[1:]:
    case ["run", day, part]:
        input_file = f"inputs/day{day}.txt"
        print(get_part_method(day, part)(input_file))
    case ["example", day, part]:
        input_file = f"examples/day{day}_example.txt"
        print(get_part_method(day, part)(input_file))
