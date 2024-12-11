from functools import cache


def part1(input_file):
    stones = load_stones(input_file)
    stones = blink_times(stones, 25)
    return sum((1 for _ in stones))


def part2(input_file):
    stones = load_stones(input_file)
    return sum(blink_cache(stone, 75) for stone in stones)


# I looked up how other solved this
# I don't think I would have come to this solution on my own
@cache
def blink_cache(stone, steps):
    if steps == 0:
        return 1
    next_step_count = steps - 1
    if stone == 0:
        return blink_cache(1, next_step_count)
    elif even_number_of_digits(stone):
        left_half, right_half = split_stone(stone)
        return blink_cache(left_half, next_step_count) + blink_cache(
            right_half, next_step_count
        )
    else:
        return blink_cache(stone * 2024, next_step_count)


def blink(stones):
    for stone in stones:
        if stone == 0:
            yield 1
        elif even_number_of_digits(stone):
            left_half, right_half = split_stone(stone)
            yield left_half
            yield right_half
        else:
            yield stone * 2024


def blink_times(stones, times):
    for _ in range(times):
        stones = blink(stones)
    return stones


def even_number_of_digits(stone):
    return len(list(str(stone))) % 2 == 0


def split_stone(stone):
    str_stone = str(stone)
    halfway = len(str_stone) // 2
    return int(str_stone[0:halfway]), int(str_stone[halfway:])


def load_stones(input_file):
    with open(input_file) as f:
        return [int(num_string) for num_string in f.read().strip().split(" ")]
