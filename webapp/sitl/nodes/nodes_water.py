import matplotlib.pyplot as plt
from geopy.distance import geodesic

def plan_drones_paths_geographic(num_drones, top_left, bottom_right, rows=10):
    lat1, lon1 = top_left
    lat2, lon2 = bottom_right

    # Ensure proper ordering of coordinates
    min_lat, max_lat = sorted([lat1, lat2])
    min_lon, max_lon = sorted([lon1, lon2])

    # Calculate total height and width in terms of distance
    total_height = geodesic((min_lat, min_lon), (max_lat, min_lon)).meters
    total_width = geodesic((min_lat, min_lon), (min_lat, max_lon)).meters

    # Divide the height into strips for each drone
    strip_height = total_height / num_drones
    paths = {}

    for drone_id in range(num_drones):
        # Determine the latitude range for this drone's strip
        start_lat = min_lat + (drone_id * strip_height / total_height) * (max_lat - min_lat)
        end_lat = start_lat + (strip_height / total_height) * (max_lat - min_lat)

        # Generate waypoints in a snake-like pattern
        path = []
        current_lat = start_lat
        step_lat = (end_lat - start_lat) / rows  # Divide the strip into rows

        while current_lat < end_lat:
            if len(path) % 2 == 0:
                # Left to right
                path.append((current_lat, min_lon))
                path.append((current_lat, max_lon))
            else:
                # Right to left
                path.append((current_lat, max_lon))
                path.append((current_lat, min_lon))

            # Move to the next row
            current_lat += step_lat

        paths[drone_id] = path

    return paths
