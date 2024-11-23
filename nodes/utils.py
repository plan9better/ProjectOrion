from Map import Map
def set_map_for_drone(drone_map: Map, drones: list):
    number_of_drones = len(drones)
    width = drone_map.top_left[0] - drone_map.top_right[0]
    drone_field_width = width // number_of_drones
    for i, drone in enumerate(drones):
        drone_top_left = drone_map.top_left[0] + i * drone_field_width
        drone_bottom_right = drone_map.bottom_left[0] + i * drone_field_width
        drone_map = Map(drone_top_left, drone_bottom_right)
        drone.setMap(drone_map)