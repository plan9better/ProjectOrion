from Map import Map

class Drone:
    def __init__(self, drone_id):
        self.drone_id = drone_id
        self.nodes = []  # List of coordinates for the flight path
        self.map = map;
    def setMap(self, map):
        if  not isinstance(map, Map):
            return

        self.map = map

    def setViewBox(self, altitude):


    def get_viewbox_area(self):
        """Calculate the area covered by the viewbox."""
        width, height = self.viewbox
        area = width * height
        print(f"Drone {self.drone_id}'s viewbox covers an area of {area} square units.")
        return area

