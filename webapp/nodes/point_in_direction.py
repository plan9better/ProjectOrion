import math

# Radius of the Earth in kilometers


def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1_rad = deg_to_rad(lat1)
    lon1_rad = deg_to_rad(lon1)
    lat2_rad = deg_to_rad(lat2)
    lon2_rad = deg_to_rad(lon2)

    # Difference in longitudes
    delta_lon = lon2_rad - lon1_rad

    # Calculate the bearing
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)

    bearing_rad = math.atan2(x, y)

    # Convert the bearing from radians to degrees
    bearing_deg = rad_to_deg(bearing_rad)

    # Normalize the bearing to be between 0 and 360 degrees
    bearing_deg = (bearing_deg + 360) % 360

    return bearing_deg
def deg_to_rad(deg):
    return deg * (math.pi / 180)


def rad_to_deg(rad):
    return rad * (180 / math.pi)


def calculate_new_coordinates(point1: tuple,point2: tuple, distance):
    # Convert the initial point from degrees to radians
    lat1=point1[0]
    lon1=point1[1]
    lat2=point2[0]
    lon2=point2[1]
    heading=calculate_bearing(point1[0], point1[1], point2[0], point2[1])
    R = 6371.0
    lat1_rad = deg_to_rad(lat1)
    lon1_rad = deg_to_rad(lon1)

    # Convert the heading from degrees to radians
    heading_rad = deg_to_rad(heading)

    # Calculate the new latitude and longitude using the formulas
    new_lat_rad = lat1_rad + (distance / R) * math.cos(heading_rad)
    new_lon_rad = lon1_rad + (distance / R) * math.sin(heading_rad) / math.cos(lat1_rad)

    # Convert the result back to degrees
    new_lat = rad_to_deg(new_lat_rad)
    new_lon = rad_to_deg(new_lon_rad)

    return (new_lat, new_lon)


# lat1 = 54.51511951567858   # Latitude of the starting point (in degrees)
# lon1 = 18.542232924301757
# lat2 = 54.51334852658739  # Latitude of the starting point (in degrees)
# lon2 = 18.544687602856936
# point1 = (lat1, lon1)
# point2 = (lat2, lon2)
# distance = 0.2# Distance to move (in kilometers)

# newPoint = calculate_new_coordinates(point1, point2, distance)
# print(newPoint[0], newPoint[1])

#54.515576,18.548518