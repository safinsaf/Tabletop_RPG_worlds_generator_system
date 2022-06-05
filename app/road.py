

class Road:
    path = []

    def __init__(self, road_enpoints, world_map, continent, terrains, bioms):
        self.terrains = terrains
        self.bioms = bioms
        self.find_road_path(road_enpoints, world_map, continent)


    def find_road_path(self, road_enpoints, world_map, continent):
        city1 = road_enpoints[0]
        city2 = road_enpoints[1]

        start_point = city1.points[0]
        end_point = city2.points[0]

        self.find_road_dijkstra(start_point, end_point, world_map, continent)

        
    def find_road_dijkstra(self, start_point, end_point, world_map, continent):
        x1 = start_point[0]
        y1 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]

        (x1_coord, y1_coord) = world_map.cells[x1][y1].center
        (x2_coord, y2_coord) = world_map.cells[x2][y2].center

        dist_original = ((x2_coord - x1_coord)**2 + (y2_coord - y1_coord)**2) ** 0.5

        radius = dist_original + world_map.size * 15
        
        all_coords = continent.coords_arr


        dijkstra_map = []
        start_index = -1
        end_index = -1
        coord_to_index = dict()
        for i in range(len(all_coords)):
            (x, y) = all_coords[i]
            (x_coord, y_coord) = world_map.cells[x][y].center

            dist = ((x_coord - x1_coord)**2 + (y_coord - y1_coord)**2) ** 0.5
            if dist < radius:
                coord_to_index[(x, y)] = len(dijkstra_map)
                dijkstra_map.append((x, y))
                

            if (x, y) == start_point:
                start_index = len(dijkstra_map) - 1
            if (x, y) == end_point:
                end_index = len(dijkstra_map) - 1
        
        #print("Point1", start_point, end_point)
        #print("Start index", start_index, "End index", end_index)
        #print("Start coord", dijkstra_map[start_index], "End coord", dijkstra_map[end_index])

        if len(dijkstra_map) == 0:
            return

        dist_dijkstra_map = [1e10 for i in range(len(dijkstra_map))]
        dist_dijkstra_map[start_index] = 0
        prev_dijkstra_map = [-1 for i in range(len(dijkstra_map))]
        visited_dijkstra_map = [0 for i in range(len(dijkstra_map))]


        # print(len(dijkstra_map))

        path_exists = True

        while True:
            min_weight = 1e10
            min_index = -1

            for i in range(len(dist_dijkstra_map)):
                if dist_dijkstra_map[i] < min_weight and visited_dijkstra_map[i] == 0:
                    min_weight = dist_dijkstra_map[i]
                    min_index = i

            visited_dijkstra_map[min_index] = 1

            if min_index == -1:
                path_exists = False
                break

            if min_index == end_index:
                break

            current_coord = dijkstra_map[min_index]

            neighbors = world_map.__find_all_neighbors__([current_coord])

            for i in range(len(neighbors)):
                (x_coord, y_coord) = neighbors[i]
                if (x_coord, y_coord) in coord_to_index:
                    next_index = coord_to_index[(x_coord, y_coord)]
                else:
                    continue

                step_weight = self.calculate_weight(world_map, neighbors[i])
                
                # print(len(dist_dijkstra_map), next_index, min_index)
                if dist_dijkstra_map[next_index] > dist_dijkstra_map[min_index] + step_weight:
                    dist_dijkstra_map[next_index] = dist_dijkstra_map[min_index] + step_weight
                    prev_dijkstra_map[next_index] = min_index

        if path_exists:
            path_indeces = [end_index]
            while path_indeces[-1] != start_index: 
                current = path_indeces[-1]
                next = prev_dijkstra_map[current]
                path_indeces.append(next)
            
            path = []
            for i in range(len(path_indeces)):
                index = path_indeces[i]
                coords = dijkstra_map[index]
                path.append(coords)

            path = path[::-1]
            

            self.path = path
            # if path[0] == start_point and path[-1] == end_point:
            #     self.path = path
            # else:
            #     self.path = []    

        else:
            self.path = []


    def calculate_weight(self, world_map, coord):
        (x, y) = coord
        terrain_type = world_map.cells[x][y].terrain_type
        biom_type = world_map.cells[x][y].biom_type
        is_river = world_map.cells[x][y].river

        weight = 0
        if terrain_type != "":
            weight += self.terrains[terrain_type]["crossing_weight"]
        else:
            weight += 1e10

        if biom_type != "":
            weight += self.bioms[biom_type]["crossing_weight"]
        else:
            weight += 1e10

        if is_river:
            weight += 200
        
        return weight





