from Map import Map
import math
def set_map_for_drone(drone_map: Map, drones: list):
    number_of_drones = len(drones)
    width = drone_map.top_left[0] - drone_map.top_right[0]
    drone_field_width = width // number_of_drones
    for i, drone in enumerate(drones):
        drone_top_left = drone_map.top_left[0] + i * drone_field_width
        drone_bottom_right = drone_map.bottom_left[0] + i * drone_field_width
        drone_map = Map(drone_top_left, drone_bottom_right)
        drone.setMap(drone_map)

def haversine(lat1, lon1, lat2, lon2):

    R = 6371.0


    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)


    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def get_area_fit_count(area1, area2):
    if (area1 < area2):
        return
    fitCount = math.ceil(area1 / area2)
    return fitCount