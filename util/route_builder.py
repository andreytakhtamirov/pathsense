import osmnx as ox


class RouteBuilder():

    def __init__(self, func_weight):
        self.existing_routes = []
        self.func_weight = func_weight

    def create_routes(self, G, start_node, end_node, routes_count) -> []:
        routes = []

        for _ in range(routes_count):
            route = ox.shortest_path(G, start_node, end_node,
                                     weight=self.weight)
            # Add this route to the collection so we
            # don't attempt to use the same paths.
            self.add_used_route(route)

            routes.append(route)

        return routes

    def add_used_route(self, route):
        self.existing_routes.append(route)

    def weight(self, u, v, edge_attr):
        weight = self.func_weight(u, v, edge_attr)

        if len(self.existing_routes) > 0:
            # Check if the path has been previously used by another
            # route. We don't want our routes to be too similar.
            for route in self.existing_routes:
                if u in route:
                    weight *= 5

        return weight
