def part1(input_file):
    connections = load_connections(input_file)
    graph = build_graph(connections)
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


def part2(input_file):
    connections = load_connections(input_file)
    graph = build_graph(connections)

    sets = set()

    def search(comp, connections):
        key = tuple(sorted(connections))
        if key in sets:
            return
        sets.add(key)
        for neighbor in graph[comp]:
            if neighbor in connections:
                continue
            if not all(neighbor in graph[query] for query in connections):
                continue
            search(neighbor, {*connections, neighbor})

    for comp in graph:
        search(comp, {comp})

    return ",".join(max(sets, key=len))


def build_graph(connections):
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph


def load_connections(input_file):
    with open(input_file) as f:
        return [tuple(row.split("-")) for row in f.read().splitlines()]
