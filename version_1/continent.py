import random

class Continent:

    start_coords = []
    coords_arr = [(10,10),(10,11),(11,10)]
    coords_dic = []
    neighbors = []
    # ID = "Africa"

    def __init__(self, start_coords, ID):

        self.ID = ID

        if type(start_coords) == list:
            self.start_coords = start_coords
            self.coords_arr = start_coords.copy()
        else:
            self.start_coords = [start_coords]
            self.coords_arr = [start_coords]


    def __free__(self, x, y, worldMap):
        if worldMap.cells[x][y].level_0 == "Ocean":
            return True
        else:
            return False



    def __find_neighbors__(self, worldMap):
        self.neighbors = []
        for el in self.coords_arr:
            d = [(0,1),(1,0),(0,-1),(-1,0),
                 (1,1),(1,-1),(-1,1),(-1,-1)]
            possible_neighbors = []
            for (dx, dy) in d:
                possible_neighbors.append((el[0]+dx, el[1]+dy))
            for (x, y) in possible_neighbors:
                if self.__free__(x, y, worldMap):
                    self.neighbors.append((x, y))

    def __increase_territory__(self, worldMap):
        new_cell = self.neighbors.pop()
        (x, y) = new_cell
        worldMap.cells[x][y].level_0 = self.ID
        R = random.randint(30, 50)
        G = random.randint(200, 220)
        B = random.randint(0, 10)
        T = random.randint(100, 102)
        worldMap.cells[x][y].color = (R, G, B, T)
        self.coords_arr.append((x,y))





    def increase_territory(self, worldMap, times):
        self.__find_neighbors__(worldMap)
        random.shuffle(self.neighbors)



        size = min(times, len(self.neighbors))
        for i in range(size):
            self.__increase_territory__(worldMap)

        left = times - size

        if left != 0:
            self.increase_territory(worldMap, left)

