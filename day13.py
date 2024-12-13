import re

a_cost = 3
b_cost = 1
correction = 10000000000000


def part1(input_file):
    machines = load_machines(input_file)
    all_combos = [find_combos(machine) for machine in machines]
    winners = find_winners(all_combos)
    cheapest = [find_cheapest(winner) for winner in winners]
    return sum(cheapest)


def part2(input_file):
    machines = load_machines(input_file)
    machines = correct_machines(machines)
    all_combos = [find_combos2(machine) for machine in machines]
    winners = find_winners(all_combos)
    cheapest = [find_cheapest(winner) for winner in winners]
    return sum(cheapest)


def correct_machines(machines):
    return [
        (a_move, b_move, (correction + prize[0], correction + prize[1]))
        for a_move, b_move, prize in machines
    ]


def find_cheapest(winner):
    prices = [calc_price(combo) for combo in winner]
    return min(prices)


def calc_price(combo):
    return combo[0] * a_cost + combo[1] * b_cost


def find_winners(all_combos):
    return [combo for combo in map(list, all_combos) if combo]


def find_combos(machine):
    a_move, b_move, prize = machine
    for a_times in range(1, 101):
        for b_times in range(1, 101):
            x_loc = a_move[0] * a_times + b_move[0] * b_times
            if x_loc > prize[0]:
                break
            if x_loc == prize[0]:
                y_loc = a_move[1] * a_times + b_move[1] * b_times
                if y_loc == prize[1]:
                    yield (a_times, b_times)


def find_combos2(machine):
    a_move, b_move, prize = machine
    # Had to watch https://www.youtube.com/watch?v=-5J-DAsWuJc
    ax, ay = a_move
    bx, by = b_move
    px, py = prize
    a_times = (px * by - py * bx) / (ax * by - ay * bx)
    b_times = (px - ax * a_times) / bx
    if a_times % 1 == b_times % 1 == 0:
        yield int(a_times), int(b_times)


def load_machines(input_file):
    machines = []
    with open(input_file) as f:
        raw_machines = f.read().split("\n\n")
        for raw_machine in raw_machines:
            raw_a_button, raw_b_button, raw_prize = raw_machine.split("\n")
            a_button = parse_button(raw_a_button)
            b_button = parse_button(raw_b_button)
            prize = parse_prize(raw_prize)
            machines.append((a_button, b_button, prize))
    return machines


button_re = r"Button ([A-Z]): X(\+)(\d{1,2}), Y(\+)(\d{1,2})"
prize_re = r"Prize: X=(\d+), Y=(\d+)"


def parse_button(raw_button):
    _, _, x, _, y = re.findall(button_re, raw_button)[0]
    return (int(x), int(y))


def parse_prize(raw_prize):
    x, y = re.findall(prize_re, raw_prize)[0]
    return (int(x), int(y))
