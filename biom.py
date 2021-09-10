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

    def __free__(self, x, y, world_map):
        return (
            world_map.in_map(x, y)
            and world_map.cells[x][y].level_0 != "Ocean"
            and world_map.cells[x][y].level_1 == "Biom"
        )

    def __increase_territory__(self, world_map):
        new_cell = self.neighbors.pop()
        (x, y) = new_cell
        R = random.randint(self.color_range[0][0], self.color_range[0][1])
        G = random.randint(self.color_range[1][0], self.color_range[1][1])
        B = random.randint(self.color_range[2][0], self.color_range[2][1])
        A = random.randint(self.color_range[3][0], self.color_range[3][1])
        world_map.cells[x][y].set_biom(self.name, (R, G, B, A))
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
        color = self.bioms[self.biom_type]["Color"]
        R = (color["R_left"], color["R_right"])
        G = (color["G_left"], color["G_right"])
        B = (color["B_left"], color["B_right"])
        A = (color["A_left"], color["A_right"])
        self.color_range = (R, G, B, A)
