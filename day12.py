from enum import Enum


def part1(input_file):
    garden = load_garden(input_file)
    plots = find_plots(garden)
    areas = [len(plot) for plot in plots]
    perimeters = [calc_perimeter(garden, plot) for plot in plots]
    prices = [area * perimeter for area, perimeter in zip(areas, perimeters)]
    return sum(prices)


def part2(input_file):
    garden = load_garden(input_file)
    plots = find_plots(garden)
    areas = [len(plot) for plot in plots]
    plot_sides = map(calc_sides, plots)
    prices = [area * sides for area, sides in zip(areas, plot_sides)]
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


def calc_sides(plot):
    sides = 0
    for coor in plot:
        # Use patterns to find the corners for the plot
        surr = get_surrounding_coors(coor)
        if surr["n"] not in plot and surr["w"] not in plot:
            sides += 1
        if surr["n"] not in plot and surr["e"] not in plot:
            sides += 1
        if surr["w"] not in plot and surr["s"] not in plot:
            sides += 1
        if surr["e"] not in plot and surr["s"] not in plot:
            sides += 1
        if surr["s"] in plot and surr["se"] in plot and surr["e"] not in plot:
            sides += 1
        if surr["e"] in plot and surr["se"] in plot and surr["s"] not in plot:
            sides += 1
        if surr["e"] in plot and surr["ne"] in plot and surr["n"] not in plot:
            sides += 1
        if surr["n"] in plot and surr["ne"] in plot and surr["e"] not in plot:
            sides += 1
    return sides


surrounding_diffs = {
    "n": (0, -1),
    "ne": (1, -1),
    "e": (1, 0),
    "se": (1, 1),
    "s": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
    "nw": (-1, -1),
}


def get_surrounding_coors(coor):
    return {
        direction: (coor[0] + diff[0], coor[1] + diff[1])
        for direction, diff in surrounding_diffs.items()
    }


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
