from metrics.constants import CYCLING_SPEED_METERS_PER_SECOND_ROAD, CYCLING_SPEED_METERS_PER_SECOND_UNPAVED, SURFACE_LABEL_PAVED, SURFACE_LABEL_UNPAVED,  SURFACE_LABEL_UNKNOWN, HIGHWAY_LABEL_UNKNOWN, SURFACES_PAVED
from util.edge_attribute_helper import are_any_paved


def metrics_from_route(Graph, route):
    surface_lengths = {}
    highway_lengths = {}
    total_length = 0
    total_time_seconds = 0

    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        edge_attributes = Graph[u][v]
        surface = edge_attributes[0].get('surface')
        length = edge_attributes[0].get('length')
        highway = edge_attributes[0].get('highway')

        if surface == None or are_any_paved(surface, SURFACES_PAVED):
            total_time_seconds += length / CYCLING_SPEED_METERS_PER_SECOND_ROAD
        else:
            total_time_seconds += length / CYCLING_SPEED_METERS_PER_SECOND_UNPAVED

        if isinstance(surface, list):
            # just take the first surface value in the array
            surface = surface[0]

        if surface:
            if are_any_paved(surface, SURFACES_PAVED):
                surface = SURFACE_LABEL_PAVED
            else:
                surface = SURFACE_LABEL_UNPAVED

            if surface in surface_lengths:
                surface_lengths[surface] += length
            else:
                surface_lengths[surface] = length

        else:
            if SURFACE_LABEL_UNKNOWN in surface_lengths:
                surface_lengths[SURFACE_LABEL_UNKNOWN] += length
            else:
                surface_lengths[SURFACE_LABEL_UNKNOWN] = length

        total_length += length

        if isinstance(highway, list):
            highway = highway[0]  # take the first highway value

        if highway:
            if highway in highway_lengths:
                highway_lengths[highway] += length
            else:
                highway_lengths[highway] = length

        else:
            if HIGHWAY_LABEL_UNKNOWN in highway_lengths:
                highway_lengths[HIGHWAY_LABEL_UNKNOWN] += length
            else:
                highway_lengths[HIGHWAY_LABEL_UNKNOWN] = length

    sorted_surface_lengths = sorted(
        surface_lengths.items(), key=lambda x: x[1], reverse=True)
    surface_lengths_data = {surface: round(
        length, 2) for surface, length in sorted_surface_lengths}

    sorted_highway_lengths = sorted(
        highway_lengths.items(), key=lambda x: x[1], reverse=True)
    highway_lengths_data = {highway: round(
        length, 2) for highway, length in sorted_highway_lengths}

    distance = round(total_length, 2)
    duration = int(round(total_time_seconds, 0))

    return distance, duration, surface_lengths_data, highway_lengths_data
