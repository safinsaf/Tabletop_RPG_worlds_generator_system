import random


class Continent:

    start_coords = []
    coords_arr = [(10, 10), (10, 11), (11, 10)]
    coords_dic = []
    neighbors = []
    # name = "Africa"

    def __init__(self, start_coords, name):

        self.name = name

        if isinstance(start_coords, list):
            self.start_coords = start_coords
            self.coords_arr = start_coords.copy()
        else:
            self.start_coords = [start_coords]
            self.coords_arr = [start_coords]

    def __free__(self, x, y, world_map):
        return world_map.in_map(x, y) and world_map.cells[x][y].level_0 == "Ocean"

    def __increase_territory__(self, world_map):
        new_cell = self.neighbors.pop()
        (x, y) = new_cell
        world_map.cells[x][y].level_0 = self.name
        R = random.randint(30, 50)
        G = random.randint(200, 220)
        B = random.randint(0, 10)
        A = random.randint(200, 210)
        world_map.cells[x][y].color = (R, G, B, A)
        self.coords_arr.append((x, y))

    def increase_territory(self, world_map, times):
        self.neighbors = world_map.__find_neighbors__(self)
        random.shuffle(self.neighbors)

        size = min(times, len(self.neighbors))
        for _ in range(size):
            self.__increase_territory__(world_map)

        left = times - size

        if left != 0:
            self.increase_territory(world_map, left)
