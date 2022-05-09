import random


class Biom:

    start_coords = []
    coords_arr = [(10, 10), (10, 11), (11, 10)]
    coords_dic = []
    neighbors = []
    color_range = ((0, 0), (0, 0), (0, 0), (0, 0))  # RGBA ranges for random

    # name = "Africa"

    def __init__(self, start_coords, name, biom_type, bioms):

        self.name = name
        self.bioms = bioms
        self.biom_type = biom_type

        if isinstance(start_coords, list):
            self.start_coords = start_coords
            self.coords_arr = start_coords.copy()
        else:
            self.start_coords = [start_coords]
            self.coords_arr = [start_coords]

        self.__set_default_color_range__()

    def is_restricted(self, x, y, world_map):
        return world_map.cells[x][y].terrain_type in self.bioms[self.biom_type]["restricted_terrains"]

    def __free__(self, x, y, world_map):
        return (
            world_map.in_map(x, y)
            and world_map.cells[x][y].level_0 != "Ocean"
            and world_map.cells[x][y].level_1 != "Terrain"
            and not self.is_restricted(x, y, world_map)
            and world_map.cells[x][y].level_2 == "Biom"
        )

    def __increase_territory__(self, world_map):
        new_cell = self.neighbors.pop()
        (x, y) = new_cell
        world_map.cells[x][y].set_biom(self.name, self.color_range, self.biom_type)
        self.coords_arr.append((x, y))

    def increase_territory(self, world_map, times):
        self.neighbors = world_map.__find_neighbors__(self)
        random.shuffle(self.neighbors)
        size = min(times, len(self.neighbors))
        if size == 0:
            return
        for _ in range(size):
            self.__increase_territory__(world_map)

        left = times - size

        if left != 0:
            self.increase_territory(world_map, left)

    def set_color_range(self, new_color_range):
        self.color_range = new_color_range

    def __set_default_color_range__(self):
        color = self.bioms[self.biom_type]["color"]
        R = (color["r_left"], color["r_right"])
        G = (color["g_left"], color["g_right"])
        B = (color["b_left"], color["b_right"])
        A = (color["a_left"], color["a_right"])
        self.color_range = (R, G, B, A)
