def part1(input_file):
    secret_numbers = load_secret_numbers(input_file)
    for _ in range(2000):
        secret_numbers = map(process, secret_numbers)
    return sum(secret_numbers)


def part2(input_file):
    secret_number = 123
    sequence = [secret_number]
    for _ in range(10 - 1):
        secret_number = process(secret_number)
        sequence.append(secret_number)
    prices = []
    for num in sequence:
        prices.append(int(str(num)[-1]))
    price_diffs = []
    for i in range(len(prices) - 1):
        price_diffs.append(prices[i + 1] - prices[i])
    return max_index_after(prices, 4), prices, price_diffs


def max_index_after(values, after):
    return max(enumerate(values[after:]), key=lambda n: n[1])[0] + after


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
