import polyline
from shapely.geometry import LineString

from convert.constants import POLYLINE_PRECISION


def route_to_polyline6(Graph, route):
    combined_coordinates = []
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        edge_attributes = Graph[u][v]
        geometry = edge_attributes.get(0).get('geometry')

        if isinstance(geometry, LineString):
            combined_coordinates.extend(list(geometry.coords))
        elif geometry != None:  # Handle multi-part geometry
            for linestring in geometry:
                combined_coordinates.extend(list(linestring.coords))

    line_string = LineString(combined_coordinates)

    coordinates = [(lat, lng) for lng, lat in line_string.coords]
    polyline6_route = polyline.encode(
        coordinates, precision=POLYLINE_PRECISION)
    return polyline6_route
