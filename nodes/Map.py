class Map:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.top_right = (top_left.index(0), bottom_right.index(1))
        self.bottom_left = (bottom_right.index(0), top_left.index(1))

    def split_to_parts(self, number_of_drones: int):
        width = self.top_left.index(0) - self.top_right.index(0)
        height = self.top_left.index(1) - self.bottom_left.index(1)

        pass

    def __str__(self):
        return (
            f"Map Corners:\n"
            f"Corner 1: {self.corner1}\n"
            f"Corner 2: {self.corner2}\n"
            f"Corner 3: {self.corner3}\n"
            f"Corner 4: {self.corner4}"
        )
