import random
from colorsys import hsv_to_rgb


class Cell:

    center = (0, 0)
    borders = [(0, 0), (0, 0), (0, 0), (0, 0)]
    color = (0, 0, 0, 0)
    border_color = (-1, -1, -1, -1)
    terrain_type = ""  # plain|hill|mountain
    biom_type = ""
    level_0 = "ocean"  # "ocean|$(name)"
    level_1 = "terrain"  # "terrain|$(name)"
    level_2 = "biom"  # "biom|$(name)"
    river = False
    city = "city"

    def __init__(self, center, borders):
        self.center = center
        self.borders = borders
        self.height = 0

    def set_height(self, height):
        self.height = height

    def set_color(self, new_color):
        self.color = new_color

    def set_color_from_range(self, color_range):
        R = random.randint(color_range[0][0], color_range[0][1])
        G = random.randint(color_range[1][0], color_range[1][1])
        B = random.randint(color_range[2][0], color_range[2][1])
        A = random.randint(color_range[3][0], color_range[3][1])
        self.set_color((R, G, B, A))

    def set_border_color(self, new_color):
        self.border_color = new_color

    def set_border_color_from_range(self, color_range):
        R = random.randint(color_range[0][0], color_range[0][1])
        G = random.randint(color_range[1][0], color_range[1][1])
        B = random.randint(color_range[2][0], color_range[2][1])
        A = random.randint(color_range[3][0], color_range[3][1])
        self.set_border_color((R, G, B, A))

    def set_continent(self, new_continent_name, color_range):
        self.level_0 = new_continent_name
        self.set_color_from_range(color_range)

    def set_terrain(self, new_terrain_name, color_range, terrain_type):
        self.level_1 = new_terrain_name
        self.terrain_type = terrain_type
        self.set_color_from_range(color_range)

    def set_biom(self, new_biom_name, color_range, biom_type):
        self.level_2 = new_biom_name
        self.biom_type = biom_type
        self.set_border_color_from_range(color_range)

    def from_hsv_to_rgb(self, hsv):

        rgb = hsv_to_rgb(
            float(hsv[0]) / 360.0,
            float(hsv[1]) / 100.0,
            float(hsv[2]) / 100.0,
        )
        return (
            int(rgb[0] * 255 + 0.5),
            int(rgb[1] * 255 + 0.5),
            int(rgb[2] * 255 + 0.5),
        )
