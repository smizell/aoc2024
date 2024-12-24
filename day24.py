def part1(input_file):
    wires = load_data(input_file)

    def get_val(maybe_wire):
        maybe_val = wires[maybe_wire]
        if type(maybe_val) == int:  # noqa: E721
            return maybe_val
        gate, maybe_a, maybe_b = maybe_val
        wires[maybe_wire] = gates[gate](get_val(maybe_a), get_val(maybe_b))
        return wires[maybe_wire]

    for wire in wires.keys():
        get_val(wire)
    z_keys = sorted([w for w in wires.keys() if w.startswith("z")], reverse=True)
    z_val_str = ""
    for k in z_keys:
        z_val_str += str(wires[k])
    z_val = int(z_val_str, 2)
    return z_val


def _and(a, b):
    if a == 1 and b == 1:
        return 1
    else:
        return 0


def _or(a, b):
    if a == 1 or b == 1:
        return 1
    else:
        return 0


def _xor(a, b):
    if a != b:
        return 1
    else:
        return 0


gates = {"AND": _and, "OR": _or, "XOR": _xor}


def load_data(input_file):
    with open(input_file) as f:
        raw_wires, raw_connections = f.read().split("\n\n")
    parsed_wires = [raw_wire.split(": ") for raw_wire in raw_wires.split("\n")]
    wires = {wire[0]: int(wire[1]) for wire in parsed_wires}
    parsed_connections = [
        raw_connection.split(" ") for raw_connection in raw_connections.split("\n")
    ]
    connections = [(c[0], c[1], c[2], c[4]) for c in parsed_connections]
    for c in parsed_connections:
        wires[c[4]] = (c[1], c[0], c[2])
    return wires
