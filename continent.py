import random


class Continent:

    start_coords = []
    coords_arr = [(10, 10), (10, 11), (11, 10)]
    coords_dic = []
    neighbors = []
    color_range = ((30, 50), (200, 220), (0, 10), (200, 210))  # RGBA ranges for random
    # name = "Africa"

    def __init__(self, start_coords, name, world_map):

        self.name = name

        if isinstance(start_coords, list):
            self.start_coords = start_coords
            self.coords_arr = start_coords.copy()
        else:
            self.start_coords = [start_coords]
            self.coords_arr = [start_coords]
        for (x, y) in self.coords_arr:
            world_map.cells[x][y].set_continent(self.name, self.color_range)

    def __free__(self, x, y, world_map):
        return world_map.in_map(x, y) and world_map.cells[x][y].level_0 == "Ocean"

    def __increase_territory__(self, world_map):
        (x, y) = self.neighbors.pop()
        world_map.cells[x][y].set_continent(self.name, self.color_range)
        self.coords_arr.append((x, y))

    def increase_territory(self, world_map, times):
        self.neighbors = world_map.__find_neighbors__(self)
        # self.neighbors = list(dict.fromkeys(self.neighbors))

        if len(self.neighbors) == 0:
            return

        random.shuffle(self.neighbors)

        size = min(times, len(self.neighbors))
        for _ in range(size):

            self.__increase_territory__(world_map)

        left = times - size

        if left != 0:
            self.increase_territory(world_map, left)

    def set_color_range(self, new_color_range):
        self.color_range = new_color_range
