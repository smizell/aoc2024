def part1(input_file):
    connections = load_connections(input_file)
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    sets_of_three = []
    for a, bs in graph.items():
        for b in bs:
            for c in graph[b]:
                if c in graph[a]:
                    value = set([a, b, c])
                    if value not in sets_of_three:
                        sets_of_three.append(value)
    sets_with_t = [s for s in sets_of_three if any(c.startswith("t") for c in s)]
    return len(sets_with_t)


def load_connections(input_file):
    with open(input_file) as f:
        return [tuple(row.split("-")) for row in f.read().splitlines()]
