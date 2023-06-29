import re

from gravel_cycling.constants import DEFAULT_WIDTH, SURFACES_PAVED, HIGHWAY_TYPES
from util.edge_attribute_helper import are_all_paved, are_any_paved, is_highway_cycle_friendly


def calculate_cyclability_score(bicycle_type, highway_type, surface_type, foot_type, length, name):
    weight = 1

    if bicycle_type == 'designated':
        if surface_type != None and not are_all_paved(surface_type, SURFACES_PAVED):
            weight = length * 100.0
            return weight
        elif (surface_type == None):
            weight = length * 5.0
            return weight
        else:
            weight = 1/length + length*0.3

    if highway_type != None and is_highway_cycle_friendly(highway_type, HIGHWAY_TYPES):
        if surface_type != None and not are_all_paved(surface_type, SURFACES_PAVED):
            weight = length * 10.0
            return weight
        elif (surface_type == None):
            weight = length * 5.0
        else:
            weight = 1/length + length*0.3
    else:
        if surface_type == None or (surface_type != None and are_all_paved(surface_type, SURFACES_PAVED)):
            weight = 1/length

    return weight


def calculate_cyclability_score_alt(bicycle_type, highway_type, surface_type, foot_type, length, name):
    weight = 1

    if surface_type != None and not are_any_paved(surface_type, SURFACES_PAVED):
        weight = 1/(length*0.6)
    elif (surface_type == None):
        weight = 1/length
    else:
        weight = 1/(length*length)

    if highway_type != None and is_highway_cycle_friendly(highway_type, HIGHWAY_TYPES):
        weight *= 0.3

    return weight


# TODO fix error given width value "0,5".
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
    name = edge_attr.get(0).get("name", "")

    # Width is unused for now.
    # width = edge_attr.get(0).get("width", DEFAULT_WIDTH)

    weight = 1/calculate_cyclability_score(
        bicycle_type, highway_type, surface_type, foot_type, length, name)

    return weight


def cycle_gravel_edge_weight_alt(u, v, edge_attr):
    bicycle_type = edge_attr.get(0).get("bicycle")
    highway_type = edge_attr.get(0).get("highway")
    surface_type = edge_attr.get(0).get("surface")
    foot_type = edge_attr.get(0).get("foot")
    length = edge_attr.get(0).get("length", 1)
    width = edge_attr.get(0).get("width", DEFAULT_WIDTH)
    name = edge_attr.get(0).get("name", "")

    weight = 1/calculate_cyclability_score_alt(
        bicycle_type, highway_type, surface_type, foot_type, length, name)

    return weight