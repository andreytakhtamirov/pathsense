def are_all_paved(road_surface, paved_list):
    if isinstance(road_surface, str):
        return road_surface in paved_list
    elif isinstance(road_surface, list):
        return all(surface in paved_list for surface in road_surface)
    else:
        raise ValueError("road_surface must be a string or a list")


def are_any_paved(road_surface, paved_list):
    if isinstance(road_surface, str):
        return road_surface in paved_list
    elif isinstance(road_surface, list):
        return any(surface in paved_list for surface in road_surface)
    else:
        raise ValueError("road_surface must be a string or a list")


def is_highway_cycle_friendly(highway_type, highway_list):
    if isinstance(highway_type, str):
        return highway_type in highway_list
    elif isinstance(highway_type, list):
        return any(highway in highway_list for highway in highway_type)
    else:
        raise ValueError("highway_type must be a string or a list")
