from itertools import groupby


def part1(input_file):
    rules, updates = load_data(input_file)
    sorted_rules = sorted(rules, key=lambda rule: rule[0])
    grouped_rules = dict(
        [
            [key, [page[1] for page in pages]]
            for key, pages in groupby(sorted_rules, key=lambda rule: rule[0])
        ]
    )
    valid_updates = [
        update for update in updates if update_is_valid(grouped_rules, update)
    ]
    middles = [find_middle(update) for update in valid_updates]
    return sum(middles)


def update_is_valid(rules, update):
    for page in update:
        page_idx = update.index(page)
        for follower_page in rules.get(page, []):
            try:
                follower_page_idx = update.index(follower_page)
                if not follower_page_idx > page_idx:
                    return False
            except ValueError:
                continue
    return True


def find_middle(update):
    return update[len(update) // 2]


def load_data(input_file):
    with open(input_file) as f:
        raw_rules, raw_updates = f.read().split("\n\n")
        return [
            [
                [int(string_number) for string_number in raw_rule.split("|")]
                for raw_rule in raw_rules.split("\n")
            ],
            [
                [int(page) for page in raw_update_line.split(",")]
                for raw_update_line in raw_updates.split("\n")
            ],
        ]
