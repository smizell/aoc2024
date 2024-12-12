def part1(input_file):
    garden = load_garden(input_file)
    plots = find_plots(garden)
    areas = [len(plot) for plot in plots]
    perimeters = [calc_perimeter(garden, plot) for plot in plots]
    prices = [area * perimeter for area, perimeter in zip(areas, perimeters)]
    return sum(prices)


def find_plots(garden):
    plotted = []
    plots = []
    for coor in every_coor(garden):
        if coor in plotted:
            continue
        plot = find_plot(garden, coor)
        plots.append(plot)
        plotted += plot
    return plots


def find_plot(garden, coor):
    plot = [coor]
    find_all_plot_plants(garden, coor, plot)
    return plot


def find_all_plot_plants(garden, coor, plot):
    plant_type = get_from_garden(garden, coor)
    for adj_plant in find_adj_plants(garden, coor, plant_type):
        if adj_plant not in plot:
            plot.append(adj_plant)
            find_all_plot_plants(garden, adj_plant, plot)


def calc_perimeter(garden, plot):
    total = 0
    for coor in plot:
        plant_type = get_from_garden(garden, coor)
        adj_plants = find_adj_plants(garden, coor, plant_type)
        fences_needed = 4 - len(adj_plants)
        total += fences_needed
    return total


adj_diffs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def find_adj_plants(garden, coor, plant_type):
    possible_coors = [
        (coor[0] + adj_diff[0], coor[1] + adj_diff[1]) for adj_diff in adj_diffs
    ]
    return [
        possible_coor
        for possible_coor in possible_coors
        if within_garden(garden, possible_coor)
        and matches_plant_type(garden, possible_coor, plant_type)
    ]


def every_coor(garden):
    for y in range(len(garden)):
        for x in range(len(garden[0])):
            yield x, y


def get_from_garden(garden, coor):
    return garden[coor[1]][coor[0]]


def matches_plant_type(garden, coor, plant_type):
    return get_from_garden(garden, coor) == plant_type


def within_garden(garden, coor):
    return len(garden[0]) > coor[0] >= 0 and len(garden) > coor[1] >= 0


def load_garden(input_file):
    with open(input_file) as f:
        return [list(row) for row in f.read().split("\n")]
