import matplotlib.pyplot as plt
from geopy.distance import distance
from point_in_direction import *
from Map import Map
from Drone import Drone
from nodes import setNodes

def plan_drones_paths_geographic(num_drones, top_left, bottom_right):
    map = Map(top_left, bottom_right)
    map.set_corners()
    drone_array = []
    drone_gap = 3
    map_height = distance(map.top_left, map.bottom_left).kilometers
    cycles_count = math.ceil(map_height/(drone_gap*num_drones))
    for i in range(num_drones):

        top_left = calculate_new_coordinates(map.top_left, map.get_bottom_left(), drone_gap*i)
        map1 = Map(top_left, map.bottom_right)
        map1.set_corners()
        drone = Drone(i)
        drone.nodes = setNodes(map1, (drone_gap*num_drones*1000,drone_gap*1000*num_drones))
        drone_array.append(drone)
    drone_paths = {}
    for drone in drone_array:
        drone_paths[drone.drone_id] = drone.nodes

    return drone_paths


def plot_drone_paths(drone_paths):
    # Create a figure for the plot
    plt.figure(figsize=(10, 6))

    # Define a set of colors for drones
    colors = plt.cm.get_cmap('tab10', len(drone_paths))

    # Offset for text labels
    text_offset = 0.001  # Adjust this value depending on the scale of your coordinates

    # Plot each drone's path
    for i, (drone_id, path) in enumerate(drone_paths.items()):
        # Extract the coordinates (assuming node is a tuple or list of (x, y))
        x_coords = [node[0] for node in path]
        y_coords = [node[1] for node in path]

        # Plot the path of the drone
        plt.plot(x_coords, y_coords, marker='o', label=f"Drone {drone_id}", color=colors(i))

        # Annotate the nodes with their index
        for idx, node in enumerate(path):
            # Offset the text slightly from the point
            plt.text(node[0] + text_offset, node[1] + text_offset, str(idx),
                     fontsize=9, color=colors(i), ha='center', va='center')

    # Add labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Drone Paths with Node Indices')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    #plot_drone_paths(plan_drones_paths_geographic(10, (10,20), (10.5, 20.5)))
    #print(plan_drones_paths_geographic(2, (10, 20), (10.5, 20.5)))







