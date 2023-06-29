import gc
import networkx as nx
from geographiclib.geodesic import Geodesic
import concurrent.futures
import math
import logging

from util.file_loader import load_pickle
from FindRoute.constants import GRAPH_PICKLE_FILE_NAME, TILE_DIMENSION_RADIUS

geod = Geodesic.WGS84


def geometry_for_coords(BLOB_SERVICE_CLIENT, CONTAINER_NAME, COORDINATE_DICT, origin_lat, origin_lon, dest_lat, dest_lon):
    Graphs = []

    # Disable garbage collection when de-pickling for performance.
    gc.disable()

    # Assume that the closest tile (center) to the coordinate will surround it enough.
    # TODO we can improve accuracy later by checking that the coordinate is indeed a reasonable distance within the tile.
    tile1 = get_closest_coord(COORDINATE_DICT, origin_lat, origin_lon)
    tile2 = get_closest_coord(COORDINATE_DICT, dest_lat, dest_lon)

    if tile1 == None or tile2 == None:
        # If either tile cannot be resolved to the available data tiles,
        # We can't get an accurate graph for them.
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        min_x = min(tile1[0], tile2[0])
        max_x = max(tile1[0], tile2[0])
        min_y = min(tile1[1], tile2[1])
        max_y = max(tile1[1], tile2[1])

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if min_x <= x <= max_x and min_y <= y <= max_y:
                    pickle_file_name = GRAPH_PICKLE_FILE_NAME.format(x, y)
                    futures.append(executor.submit(
                        load_pickle, BLOB_SERVICE_CLIENT, CONTAINER_NAME, pickle_file_name))

        for future in concurrent.futures.as_completed(futures):
            graph = future.result()
            if graph is not None:
                Graphs.append(graph)

    gc.enable()

    logging.info(f'Loaded {len(Graphs)} graphs')

    # Create big graph of tiles
    G = nx.compose_all(Graphs)

    return G


def get_closest_coord(coord_dict, origin_lat, origin_lon):
    closest_distance = math.inf
    for coord, tile_idx in coord_dict.items():
        result = geod.Inverse(origin_lat, origin_lon, coord[0], coord[1])
        distance = result['s12']

        if distance < closest_distance:
            closest_distance = distance
            closest_index = tile_idx

    if closest_distance > TILE_DIMENSION_RADIUS * 2:
        # Coordinate still lies outside the closest tile.
        # It must be in an unsupported region.
        return None
    return closest_index
