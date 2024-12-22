from itertools import cycle


def part1(input_file):
    secret_numbers = load_secret_numbers(input_file)
    for _ in range(2000):
        secret_numbers = map(process, secret_numbers)
    return sum(secret_numbers)


def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def process(secret_number):
    return process3(process2(process1(secret_number)))


def process1(secret_number):
    return prune(mix(secret_number, secret_number * 64))


def process2(secret_number):
    return prune(mix(secret_number, int(secret_number / 32)))


def process3(secret_number):
    return prune(mix(secret_number, secret_number * 2048))


def load_secret_numbers(input_file):
    with open(input_file) as f:
        return list(map(int, f.read().splitlines()))
