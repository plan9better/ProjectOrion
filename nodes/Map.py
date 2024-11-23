class Map:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.top_right = None
        self.bottom_left = None

    def set_corners(self):
        self.top_right = (self.bottom_right[0], self.top_left[1])
        self.bottom_left = (self.top_left[0], self.bottom_right[1])

    def get_top_left(self):
        return self.top_left

    def get_bottom_right(self):
        return self.bottom_right

    def get_top_right(self):
        return self.top_right

    def get_bottom_left(self):
        return self.bottom_left

    def __str__(self):
        return (
            f"Map Corners:\n"
            f"Corner 1: {self.top_left}\n"
            f"Corner 2: {self.top_right}\n"
            f"Corner 3: {self.bottom_right}\n"
            f"Corner 4: {self.bottom_left}\n"
        )
