import random


class Continent:

    start_coords = []
    coords_arr = [(10, 10), (10, 11), (11, 10)]
    neighbors = []
    color_range = ((30, 50), (200, 220), (0, 10), (200, 210))  # RGBA ranges for random
    cities = []
    name = ""

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

        world_map.continents.append(self)


    def __free__(self, x, y, world_map):
        return world_map.in_map(x, y) and world_map.cells[x][y].level_0 == "ocean"

    # def __is_near_other_continent__(self, x, y, continent, world_map):
    #     neigh0 = self.__find_all_coasts__(world_map)
    #     neigh1 = world_map.__find_all_neighbors__([(x, y)])
    #     neigh2 = 
    #     neigh3 = 


    def __increase_territory__(self, world_map):
        cell = self.neighbors.pop()
        self.__add_to_continent__(cell, world_map)

    def increase_territory(self, world_map, times):
        self.update_neighbors(world_map)

        if len(self.neighbors) == 0:
            return

        random.shuffle(self.neighbors)

        size = min(times, len(self.neighbors))
        for _ in range(size):

            self.__increase_territory__(world_map)

        left = times - size

        if left != 0:
            self.increase_territory(world_map, left)

    def __add_to_continent__(self, cell, world_map):
        (x, y) = cell
        world_map.cells[x][y].set_continent(self.name, self.color_range)
        self.coords_arr.append((x, y))
    

    def fill_holes(self, world_map):
        is_last = True

        coasts = world_map.__find_neighbors__(self)
        coasts = list(dict.fromkeys(coasts))

        components = self.__connectivity_components__(coasts, world_map)
        counter = {}
        for i in range(len(components)):
            if components[i] not in counter:
                counter[components[i]] = 0
            counter[components[i]] += 1
        items = counter.items()
        items = [(y, x) for (x, y) in items]
        items = sorted(items)
        main_component = items[-1][1]
        # print(items)

        for i in range(0, len(components)):
            if components[i] == main_component:
                continue

            cell = coasts[i]
            self.__add_to_continent__(cell, world_map)
            is_last = False
        if not is_last:
            self.fill_holes(world_map)

    def __connectivity_components__(self, coasts, world_map):
        vertices = coasts
        edges = [[] for i in range(len(vertices))]
        for i in range(len(vertices)):
            for j in range(len(vertices)):
                if i == j:
                    continue
                neighbors_i = world_map.__find_all_neighbors__([vertices[i]])
                if vertices[j] not in neighbors_i:
                    continue
                edges[i].append(j)
                edges[j].append(i)

        components = [-1] * len(vertices)
        number_of_components = 0
        for vertex in range(len(vertices)):
            if components[vertex] != -1:
                continue
            path = [vertex]
            components[vertex] = number_of_components
            while len(path) > 0:
                current = path[-1]
                for i in range(len(edges[current])):
                    neighbor = edges[current][i]
                    if components[neighbor] == -1:
                        path.append(neighbor)
                        components[neighbor] = number_of_components
                        break
                else:
                    path.pop()
            number_of_components += 1

        return components

    def set_color_range(self, new_color_range):
        self.color_range = new_color_range

    def update_neighbors(self, world_map):
        self.neighbors = world_map.__find_neighbors__(self)
        self.neighbors = list(dict.fromkeys(self.neighbors))
        self.neighbors = self.remove_near_other_continents(self.neighbors, world_map)

    def remove_near_other_continents(self, cells, world_map):
        new_cells = []
        for i in range(len(cells)):
            (x, y) = cells[i]
            if not self.is_other_continent_near(x, y, world_map):
                new_cells.append(cells[i])
        return new_cells

    def is_other_continent_near(self, x, y, world_map):
        neighbors = world_map.__find_all_neighbors__([(x, y)])
        is_edge = any(
            world_map.cells[i][j].level_0 != "ocean" and world_map.cells[i][j].level_0 != self.name for (i, j) in neighbors
        )
        return is_edge

    def __find_all_coasts__(self, world_map):
        coasts = []
        for (x, y) in self.coords_arr:
            neighbors = world_map.__find_all_neighbors__([(x, y)])
            is_edge = any(
                world_map.cells[i][j].level_0 == "ocean" for (i, j) in neighbors
            )
            if not is_edge:
                continue
            coasts.append((x, y))
        return coasts


    def all_cell_indexes(self):
        cells = self.coords_arr
        return cells

    def all_cell_coords(self, world_map):
        cells = []
        for index in self.coords_arr:
            cells.append(world_map.cells[index[0]][index[1]].center)
        return cells