from Drone import Drone
from utils import set_map_for_drone
from point_in_direction import *
from Map import Map
from geopy.distance import distance

def generate_nodes(coordinate1: tuple, coordinate2: tuple, no_drones: int, altitude: dict):
    map1 = Map(coordinate1, coordinate2)
    map1.set_corners()
    drones = []
    for id in (altitude.keys()):
        drones.append(Drone(id))
    set_map_for_drone(map1, drones)
    return_nodes = {}
    for drone in (drones):
        drone.setViewBox(altitude[drone.drone_id], 90)
        return_nodes[drone.drone_id] = setNodes(drone.map,drone.viewbox)
    return return_nodes


def setNodes(map: Map, view_box: tuple):
    nodes = []
    nh_count = 0
    map_height = distance(map.get_top_left(), map.get_bottom_left()).meters
    count = math.ceil(map_height/view_box[1])
    nodes_left = []
    nodes_right = []
    for i in range(count):
        if i == 0:
            nodes_left.append(map.get_top_left())
            nodes_right.append(map.get_top_right())
            continue
        nodes_left.append(calculate_new_coordinates(nodes_left[i-1], map.get_bottom_left(), view_box[0]/1000))
        nodes_right.append(calculate_new_coordinates(nodes_right[i-1], map.get_bottom_right(), view_box[0]/1000))
    for i in range(count):
        if i % 2 == 0:
            nodes.append(nodes_left[i])
            nodes.append(nodes_right[i])
        elif i % 2 == 1:
            nodes.append(nodes_right[i])
            nodes.append(nodes_left[i])

    return nodes

if __name__ == '__main__':
    map = Map((54.515264385561615, 18.545395708475173),(54.513271396309584, 18.539623594789287))
    map.set_corners()
    # print(setNodes(map, (100,100)))
    print(generate_nodes((54.515264385561615, 18.545395708475173),(54.513271396309584, 18.539623594789287),3,{1 : 100, 2 : 100, 3: 100}))
