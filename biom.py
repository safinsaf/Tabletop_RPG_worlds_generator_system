import random


class Biom:

    start_coords = []
    coords_arr = [(10, 10), (10, 11), (11, 10)]
    coords_dic = []
    neighbors = []

    # ID = "Africa"

    def __init__(self, start_coords, ID, biom_type, bioms):

        self.ID = ID
        self.bioms = bioms
        self.biom_type = biom_type

        if isinstance(start_coords, list):
            self.start_coords = start_coords
            self.coords_arr = start_coords.copy()
        else:
            self.start_coords = [start_coords]
            self.coords_arr = [start_coords]

    def __free__(self, x, y, worldMap):
        return (
            worldMap.cells[x][y].level_0 != "Ocean"
            and worldMap.cells[x][y].level_1 == "Biom"
        )

    def __find_neighbors__(self, worldMap):
        self.neighbors = []
        for el in self.coords_arr:
            d = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            possible_neighbors = []
            for (dx, dy) in d:
                possible_neighbors.append((el[0] + dx, el[1] + dy))
            for (x, y) in possible_neighbors:
                if self.__free__(x, y, worldMap):
                    self.neighbors.append((x, y))

    def __increase_territory__(self, worldMap):
        new_cell = self.neighbors.pop()
        (x, y) = new_cell
        worldMap.cells[x][y].level_1 = self.ID
        color = self.bioms[self.biom_type]["Color"]
        R = random.randint(color["R_left"], color["R_right"])
        G = random.randint(color["G_left"], color["G_right"])
        B = random.randint(color["B_left"], color["B_right"])
        A = random.randint(color["A_left"], color["A_right"])
        worldMap.cells[x][y].color = (R, G, B, A)
        self.coords_arr.append((x, y))

    def increase_territory(self, worldMap, times):
        self.__find_neighbors__(worldMap)
        random.shuffle(self.neighbors)

        size = min(times, len(self.neighbors))
        if size == 0:
            return
        for _ in range(size):
            self.__increase_territory__(worldMap)

        left = times - size

        if left != 0:
            self.increase_territory(worldMap, left)
