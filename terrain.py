import random


class Terrain:
    start_coords = []
    coords_arr = [(10, 10), (10, 11), (11, 10)]
    neighbors = []
    name = "Africa"
    terrain_type = ""  # Plane|Hill|Mountain
    terrains = {}
    internals = []
    color_range = [(0, 0), (0, 0), (0, 0), (0, 0)]

    all_heights = [1, 2, 3, 4, 5]
    plain_distribution = [0.7, 0.3, 0, 0, 0]
    hill_distribution = [0.1, 0.7, 0.2, 0, 0]
    mountain_distribution = [0.0, 0.05, 0.25, 0.3, 0.4]

    def __init__(self, start_coords, name, terrain_type, world_map, terrains):

        self.name = name
        self.terrain_type = terrain_type
        self.terrains = terrains
        self.__set_default_color_range__()

        if isinstance(start_coords, list):
            self.start_coords = start_coords
            self.coords_arr = start_coords.copy()
        else:
            self.start_coords = [start_coords]
            self.coords_arr = [start_coords]
        for (x, y) in self.coords_arr:
            world_map.cells[x][y].set_terrain(name, self.color_range, terrain_type)

    def __free__(self, x, y, world_map):
        return (
            world_map.in_map(x, y)
            and world_map.cells[x][y].level_0 != "Ocean"
            and world_map.cells[x][y].level_1 == "Terrain"
        )

    def __increase_territory__(self, world_map):
        new_cell = self.neighbors.pop()
        (x, y) = new_cell
        world_map.cells[x][y].set_terrain(
            self.name, self.color_range, self.terrain_type
        )
        self.coords_arr.append((x, y))

    def increase_territory(self, world_map, times):
        self.neighbors = world_map.__find_neighbors__(self)
        self.neighbors = list(dict.fromkeys(self.neighbors))
        if len(self.neighbors) == 0:
            return

        random.shuffle(self.neighbors)

        size = min(times, len(self.neighbors))
        for _ in range(size):
            self.__increase_territory__(world_map)

        left = times - size

        if left != 0:
            self.increase_territory(world_map, left)

    def __neighbors_types__(self, neighbors, world_map):
        result = []
        for (x, y) in neighbors:
            if world_map.cells[x][y].level_0 == "Ocean":
                result.append("Ocean")
            elif world_map.cells[x][y].level_1 != "Terrain":
                result.append(world_map.cells[x][y].terrain_type)
        return result

    def __set_height_edges__(self, world_map):
        for (x, y) in self.coords_arr:
            neighbors = world_map.__find_all_neighbors__([(x, y)])
            is_edge = any(
                world_map.cells[i][j].level_1 != self.name for (i, j) in neighbors
            )
            if not is_edge:
                continue

            neighbors_types = self.__neighbors_types__(neighbors, world_map)

            if "Ocean" in neighbors_types:
                world_map.cells[x][y].set_height(1)
                # world_map.cells[x][y].set_color_from_range(((0,10),(0,10),(0,10),(100,102)))
                # print(x, y, world_map.cells[x][y].height)
                # print(neighbors)
                # print(neighbors_types)
            elif self.terrain_type == "Hill":
                world_map.cells[x][y].set_height(2)
            elif self.terrain_type == "Mountain":
                world_map.cells[x][y].set_height(2)
            elif self.terrain_type == "Plain" and (
                "Mountain" in neighbors_types or "Hill" in neighbors_types
            ):
                world_map.cells[x][y].set_height(2)
            else:
                world_map.cells[x][y].set_height(1)

    def __set_height_internal__(self, world_map):

        internals = []
        for (x, y) in self.coords_arr:
            neighbors = world_map.__find_all_neighbors__([(x, y)])
            is_internal = all(
                world_map.cells[i][j].level_1 == self.name for (i, j) in neighbors
            )
            if not is_internal:
                continue
            internals.append((x, y))

        for (x, y) in internals:
            height = 0
            if self.terrain_type == "Plain":
                height = random.choices(self.all_heights, self.plain_distribution)
            elif self.terrain_type == "Hill":
                height = random.choices(self.all_heights, self.hill_distribution)
            elif self.terrain_type == "Mountain":
                height = random.choices(self.all_heights, self.mountain_distribution)
            world_map.cells[x][y].set_height(height[0])
        self.internals = internals

    def __set_color_from_height__(self, world_map):
        for (x, y) in self.coords_arr:
            HSV_color = self.terrains[self.terrain_type]["ColorHSV"]
            H = HSV_color["H"]
            S = HSV_color["S"]
            V_left = HSV_color["V_left"]
            V_right = HSV_color["V_right"]
            V = V_left + (V_right - V_left) * (
                ((world_map.cells[x][y].height - 1)) / (len(self.all_heights) - 1)
            )
            color = world_map.cells[x][y].from_hsv_to_rgb((int(H), int(S), int(V)))
            world_map.cells[x][y].set_color(color)

    def set_height(self, world_map):
        self.__set_height_edges__(world_map)
        self.__set_height_internal__(world_map)
        self.__errosion__(world_map)
        self.__errosion__(world_map)
        self.__set_color_from_height__(world_map)

    def set_color_range(self, new_color_range):
        self.color_range = new_color_range

    def __set_default_color_range__(self):
        color = self.terrains[self.terrain_type]["Color"]
        R = (color["R_left"], color["R_right"])
        G = (color["G_left"], color["G_right"])
        B = (color["B_left"], color["B_right"])
        A = (color["A_left"], color["A_right"])
        self.color_range = (R, G, B, A)

    def __errosion__(self, world_map):
        for (x, y) in self.internals:
            neighbors = world_map.__find_all_neighbors__([(x, y)])
            for (i, j) in neighbors:
                if world_map.cells[x][y].height - world_map.cells[i][j].height > 1:
                    world_map.cells[x][y].height = world_map.cells[i][j].height + 1
