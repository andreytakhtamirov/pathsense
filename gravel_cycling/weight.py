import re

from gravel_cycling.constants import DEFAULT_WIDTH, HIGHWAY_TYPE, SURFACES_PAVED


def calculate_cyclability_score(bicycle_type, highway_type, surface_type, foot_type, width, length, name):
    weight = 1

    if bicycle_type == 'designated':
        if surface_type != None and not is_paved(surface_type, SURFACES_PAVED):
            weight = length * 100.0
            return weight
        elif (surface_type == None):
            weight = length * 5.0
            return weight
        else:
            weight = 1/length + length*0.3

    if highway_type != None and is_highway_cycle_friendly(highway_type, HIGHWAY_TYPE):
        if surface_type != None and not is_paved(surface_type, SURFACES_PAVED):
            weight = length * 10.0
            return weight
        elif (surface_type == None):
            weight = length * 5.0
        else:
            weight = 1/length + length*0.3
    else:
        if surface_type == None or (surface_type != None and is_paved(surface_type, SURFACES_PAVED)):
            weight = 1/length

    return weight


def is_paved(way_surface, paved_list):
    if isinstance(way_surface, str):
        return way_surface in paved_list
    elif isinstance(way_surface, list):
        return all(surface in paved_list for surface in way_surface)
    else:
        raise ValueError("way_surface must be a string or a list")


def is_highway_cycle_friendly(way_highway, highway_list):
    if isinstance(way_highway, str):
        return way_highway in highway_list
    elif isinstance(way_highway, list):
        return any(highway in highway_list for highway in way_highway)
    else:
        raise ValueError("way_highway must be a string or a list")


def extract_width(width):
    if isinstance(width, list):
        numbers = [float(num) for num in width]
        final_width = max(numbers)
    elif isinstance(width, str):
        match = re.search(r"[-+]?\d*\.\d+|\d+", width)
        if match:
            final_width = float(match.group())
        else:
            final_width = None
    elif isinstance(width, int) or isinstance(width, float):
        final_width = width
    else:
        final_width = float(DEFAULT_WIDTH)

    return final_width


def cycle_gravel_edge_weight(u, v, edge_attr):
    bicycle_type = edge_attr.get(0).get("bicycle")
    highway_type = edge_attr.get(0).get("highway")
    surface_type = edge_attr.get(0).get("surface")
    foot_type = edge_attr.get(0).get("foot")
    length = edge_attr.get(0).get("length", 1)
    width = edge_attr.get(0).get("width", DEFAULT_WIDTH)
    name = edge_attr.get(0).get("name", "")

    width = extract_width(width)

    weight = 1/calculate_cyclability_score(
        bicycle_type, highway_type, surface_type, foot_type, width, length, name)

    return weight
