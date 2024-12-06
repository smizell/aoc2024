from itertools import groupby


def part1(input_file):
    rules, updates = prepared_data(input_file)
    valid_updates = [update for update in updates if update_is_valid(rules, update)]
    middles = [find_middle(update) for update in valid_updates]
    return sum(middles)


def part2(input_file):
    rules, updates = prepared_data(input_file)
    invalid_updates = [
        update for update in updates if not update_is_valid(rules, update)
    ]
    fixed_updates = [fix_update(rules, update) for update in invalid_updates]
    middles = [find_middle(update) for update in fixed_updates]
    return sum(middles)


def prepared_data(input_file):
    rules, updates = load_data(input_file)
    sorted_rules = sorted(rules, key=lambda rule: rule[0])
    grouped_rules = dict(
        [
            [key, [page[1] for page in pages]]
            for key, pages in groupby(sorted_rules, key=lambda rule: rule[0])
        ]
    )
    return grouped_rules, updates


def fix_update(rules, update):
    invalid_pages = [page for page in update if not page_is_valid(rules, update, page)]
    fixed_update = fix_pages(rules, update[:], invalid_pages)
    return fixed_update


def fix_pages(rules, update, invalid_pages):
    page_idxs = [update.index(page) for page in invalid_pages]
    for page_idx, page in zip(page_idxs, invalid_pages):
        follower_idxs = []
        for follower_page in rules[page]:
            try:
                follower_idxs.append(update.index(follower_page))
            except ValueError:
                continue
        location = min(follower_idxs)
        # We should be able to do this because we can only go left.
        # If we went right we would throw off the indexes.
        update.insert(location, update.pop(page_idx))
    return update


def update_is_valid(rules, update):
    for page in update:
        if not page_is_valid(rules, update, page):
            return False
    return True


def page_is_valid(rules, update, page):
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
