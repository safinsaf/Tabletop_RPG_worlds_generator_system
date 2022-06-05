import random


class City:
    name = ""
    points = [] #[(x1, y1),(x2,x2),(x3,y3)]
    port = False # False or (x, y)

    def __init2__(self, name, continent, world_map, coords=(-1, -1)):
        self.name = name
        points = continent.coords_arr
        random.shuffle(points)
        for (x1, y1) in points:
            if not world_map.cells[x1][y1].river:
                continue
            if world_map.cells[x1][y1].city != "no_city":
                continue
            height = world_map.cells[x1][y1].height
            neighbors = world_map.__find_all_neighbors__([(x1, y1)])
            random.shuffle(neighbors)
            area = [(x1, y1)]
            for (x2, y2) in neighbors:
                if world_map.cells[x2][y2].city != "no_city":
                    continue
                if world_map.cells[x2][y2].height == height:
                    area.append((x2, y2))

                if len(area) == 3:
                    self.points = area
                    self.sign(world_map)
                    return

    def sign(self, world_map):
        for (x, y) in self.points:
            world_map.cells[x][y].city = self.name
        suburb = self.points.copy()
        for i in range(3):
            for (x, y) in suburb:
                new_points = world_map.__find_all_neighbors__([(x, y)])
                suburb += new_points
                suburb = list(set(suburb))
        for (x, y) in suburb:
            if world_map.cells[x][y].city == "no_city":
                world_map.cells[x][y].city = self.name + "suburb"

    def assign_initial_coords(self, coords, continent):
        if coords == (-1,-1):
            points = continent.coords_arr
            random.shuffle(points)
            coords = points[0]
        return coords


    def find_local(self, coords, r, continent, world_map):
        locals = [[coords]]
        for i in range(r):
            new_wave = []
            for coord in locals[i]:
                new_neighbors = world_map.__find_all_neighbors__([coord])
                new_wave += new_neighbors
            new_wave = set(new_wave)
            for j in range(i+1):
                new_wave -= set(locals[j])
            locals.append(list(new_wave))
        return locals

    def compute_func(self, value, level):
        return value * (0.7)**level + max(1-level, 0) * 10 * value

    def compute_attraction(self, locals, continent, world_map):
        weight = 0
        attractors = self.races[self.race]["cities"]["attractors"]
        unique = attractors["unique"]
        bioms = attractors["biomes"]
        terrains = attractors["terrains"]


        for level in range(len(locals)):
            for coord in locals[level]:
                (x, y) = coord
                if world_map.cells[x][y].level_0 == "ocean" and \
                        "ocean" in unique:
                    weight += self.compute_func(unique["ocean"], level)
                if world_map.cells[x][y].river and \
                        "river" in unique:
                    weight += self.compute_func(unique["river"], level)
                if world_map.cells[x][y].city != "city" and \
                        "city" in unique:
                    weight += self.compute_func(unique["city"], level)
                if world_map.cells[x][y].level_2 != "biom" and \
                        world_map.cells[x][y].level_2 in bioms:
                    weight += self.compute_func(bioms[world_map.cells[x][y].level_2], level)


        #print(locals[0][0], weight)
        return weight


    def search_max_placement(self, coords, depth1, depth2, continent, world_map):
        # depth1 - 
        # depth2 - 
        jump_neighbors = self.find_local(coords, depth1, continent, world_map)
        computation_neighbors = self.find_local(coords, depth2, continent, world_map)
        weight = self.compute_attraction(computation_neighbors, continent, world_map)

        max_weight = -1e10
        max_coords = coords
        for level in range(1, len(jump_neighbors)):
            for j in range(len(jump_neighbors[level])):
                new_coords = jump_neighbors[level][j]
                (x, y) = new_coords
                if world_map.cells[x][y].level_0 == "ocean":
                    continue
                new_locals = self.find_local(new_coords, depth2, continent, world_map)
                new_weight = self.compute_attraction(new_locals, continent, world_map)
                if new_weight > max_weight:
                    max_weight = new_weight
                    max_coords = new_coords
        #print(jump_neighbors[0][0], max_coords)
        #print(max_weight)
        if jump_neighbors[0][0] == max_coords:
            return max_coords
        elif max_weight > weight:
            return self.search_max_placement(max_coords, depth1, depth2, continent, world_map)
        else:
            return max_coords

    def grow_city(self, max_coords, world_map, size = 3):
        (x1, y1) = max_coords
        self.points = [max_coords]
        height = world_map.cells[x1][y1].height
        neighbors = world_map.__find_all_neighbors__([(x1, y1)])
        random.shuffle(neighbors)
        for (x2, y2) in neighbors:
            if world_map.cells[x2][y2].level_0 == "ocean":
                continue
            if world_map.cells[x2][y2].city != "city":
                continue
            if world_map.cells[x2][y2].height == height:
                self.points.append((x2, y2))

            if len(self.points) == size:
                return

    def __init__(self, name, continent, world_map, races, race="human", coords=(-1, -1)):
        self.name = name
        self.race = race
        self.races = races
        coords = self.assign_initial_coords(coords, continent)
        coords = self.search_max_placement(coords, 10, 6, continent, world_map)
        (x, y) = coords
        self.grow_city(coords, world_map, 3)
        world_map.cells[x][y].city = self.name
        continent.cities.append(self)
        self.create_port_optional(continent, world_map)



    def create_port_optional(self,continent,world_map):
        for i in range(len(self.points)):
            (x,y) = self.points[i]
            #print("checking point", (x,y))
            #print("    river:", world_map.cells[x][y].river)
            #print("    terrain type", world_map.cells[x][y].terrain_type)
            if world_map.cells[x][y].river and world_map.cells[x][y].terrain_type != "mountain":
                #print("city_points", self.points)
                #print("river port_point:", (x,y))
                #print("river:", world_map.cells[x][y].river)
                self.__create_port__((x,y))
                return True
            

            coasts = continent.__find_all_coasts__(world_map)
            if (x,y) in coasts:
                #print("sea port_point:", (x,y))
                self.__create_port__((x,y))
                return True

            
        return False


    def __create_port__(self, point):
        self.port = point
        