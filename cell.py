import random


class Cell:

    center = (0, 0)
    borders = [(0, 0), (0, 0), (0, 0), (0, 0)]
    color = (0, 0, 0, 0)
    terrain_type = ""  # Plain|Hill|Mountain
    level_0 = "Ocean"  # "Ocean|$(name)"
    level_1 = "Terrain"  # "Terrain|$(name)"
    level_2 = "Biom"  # "Biom|$(name)"

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

    def set_continent(self, new_continent_name, color_range):
        self.level_0 = new_continent_name
        self.set_color_from_range(color_range)

    def set_terrain(self, new_terrain_name, color_range, terrain_type):
        self.level_1 = new_terrain_name
        self.terrain_type = terrain_type
        self.set_color_from_range(color_range)

    def set_biom(self, new_biom_name, color_range):
        self.level_2 = new_biom_name
        self.set_color_from_range(color_range)
