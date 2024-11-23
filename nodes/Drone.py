from Map import Map
import math
from utils import haversine



class Drone:
    def __init__(self, drone_id, camerAngle = 90):
        self.drone_id = drone_id
        self.nodes = []
        self.map = None
    def setMap(self, map):
        if  not isinstance(map, Map):
            return

        self.map = map
    def setViewBox(self, altitude, cameraAngle):
        cameraAngle_rad = math.radians(cameraAngle/2)
        width = math.tan(cameraAngle_rad) * altitude * 2
        height = math.tan(cameraAngle_rad) * altitude * 2
        self.viewbox = (width, height)

    def get_viewbox_area(self):
        width, height = self.viewbox
        area = width * height
        return area
    def get_map_area(self):
        if( not isinstance(self.map, Map)) :
            return
        bottomRight = self.map.get_bottom_right()
        bottomLeft  = self.map.get_bottom_left()
        topLeft = self.map.get_top_left()
        topRight = self.map.get_top_right()
        height = haversine(bottomRight[0], bottomRight[1], topRight[0], topRight[1])
        width = haversine(bottomLeft[0], bottomLeft[1], bottomRight[1], bottomRight[1])
        return height*width

    def createNodes(self):
        limitRight = self.map.get_top_right()
        limitBottom = self.map.get_bottom_left()


