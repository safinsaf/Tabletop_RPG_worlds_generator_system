import random
from math import sqrt

from scipy.spatial import Voronoi

from cell import Cell
from road import Road


class Map:

    H, W = 0, 0
    size = 0
    cells = []
    map_type = ""  # HEX|VORONOI
    # cells = [[Cell, Cell],[Cell, Cell]]
    rivers = []
    cities = []
    continents = []
    all_road_endpoints = []
    odd_road_endpoints = []
    roads = []

    def __init__(self, w=500, h=300, size=30, map_type="VORONOI"):
        self.W = w
        self.H = h
        self.size = size
        self.cells = []
        self.map_type = map_type
        self.create_map()

    def __grid__(self, i, j):
        if self.map_type == "VORONOI":
            return (
                self.size * (i + random.random()),
                self.size * (j + random.random()),
            )
        elif self.map_type == "HEX":
            if i % 2 == 0:
                x = self.size * (i) * (3 / 4)
                y = self.size * j * sqrt(3) / 2
                return (x, y)
            else:
                x = self.size * (i) * (3 / 4)
                y = self.size * j * sqrt(3) / 2 + self.size * sqrt(3) / 4
                return (x, y)
        else:
            raise Exception("Incorrect map_type")

    def __voronoi_neighbors__(self):
        neigbors = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        return neigbors

    def __hex_even_neighbors__(self):
        neigbors_even = [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)]
        return neigbors_even

    def __hex_odd_neighbors__(self):
        neigbors_odd = [(0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
        return neigbors_odd

    def __find_neighbors__(self, area_object):
        neighbors = []
        for el in area_object.coords_arr:
            d = []
            if self.map_type == "VORONOI":
                d = self.__voronoi_neighbors__()
            elif self.map_type == "HEX":
                if el[0] % 2 == 0:
                    d = self.__hex_even_neighbors__()
                elif el[0] % 2 == 1:
                    d = self.__hex_odd_neighbors__()
            possible_neighbors = []
            for (dx, dy) in d:
                possible_neighbors.append((el[0] + dx, el[1] + dy))

            for (x, y) in possible_neighbors:
                if self.in_map(x, y) and area_object.__free__(x, y, self):
                    neighbors.append((x, y))
        return neighbors

    def __find_all_neighbors__(self, elements):
        neighbors = []
        for el in elements:
            d = []
            if self.map_type == "VORONOI":
                d = self.__voronoi_neighbors__()
            elif self.map_type == "HEX":
                if el[0] % 2 == 0:
                    d = self.__hex_even_neighbors__()
                elif el[0] % 2 == 1:
                    d = self.__hex_odd_neighbors__()
            possible_neighbors = []
            for (dx, dy) in d:
                possible_neighbors.append((el[0] + dx, el[1] + dy))

            for (x, y) in possible_neighbors:
                if self.in_map(x, y):
                    neighbors.append((x, y))
        return neighbors

    def __create_voronoi__(self, centers):

        centers_merged = []
        for i in range(self.H):
            for j in range(self.W):
                centers_merged.append(centers[i][j])
        voronoi = Voronoi(centers_merged)

        vertices = voronoi.vertices
        regions = voronoi.regions
        point_region = voronoi.point_region

        cell_regions = [[[] for j in range(self.W)] for i in range(self.H)]

        for row in range(self.H):
            for col in range(self.W):
                cur_ind = point_region[row * (self.W) + col]
                cur_reg = regions[cur_ind]
                for el in cur_reg:

                    point = vertices[el]
                    point = tuple(point)
                    # point = (point[1], point[0])
                    cell_regions[row][col].append(point)

        return cell_regions

    def __create_cells__(self, centers, cell_regions):
        cells = []

        for i in range(self.H):
            cells.append([])
            for j in range(self.W):
                new_cell = Cell(centers[i][j], cell_regions[i][j])
                R = random.randint(0, 10)
                G = random.randint(0, 10)
                B = random.randint(245, 255)
                T = random.randint(100, 102)
                new_cell.color = (R, G, B, T)
                cells[i].append(new_cell)

        return cells

    def __generate_voronoi_map__(self):
        centers = [[self.__grid__(i, j) for j in range(self.W)] for i in range(self.H)]

        cell_borders = self.__create_voronoi__(centers)

        # centers = [
        #     [centers[i][j] for j in range(self.W)] for i in range(self.H)
        # ]

        self.cells = self.__create_cells__(centers, cell_borders)

    def __generate_hex_map__(self):
        centers = [[self.__grid__(i, j) for j in range(self.W)] for i in range(self.H)]

        cell_borders = []
        for i in range(self.H):
            cell_borders.append([])
            for j in range(self.W):
                cur_center = centers[i][j]
                a = sqrt(3) / 4
                b = 1 / 4
                c = 1 / 2
                d = [(c, 0), (b, a), (-b, a), (-c, 0), (-b, -a), (b, -a)]

                cur_borders = []
                for z in d:
                    k = z
                    # k = (z[1], z[0])
                    cur_borders.append(
                        (
                            cur_center[0] + (k[0]) * self.size,
                            cur_center[1] + (k[1]) * self.size,
                        )
                    )

                cell_borders[i].append(cur_borders)

        # centers = [
        #     [centers[i][j] for j in range(1, self.W + 1)] for i in range(1, self.H + 1)
        # ]
        # cell_borders = [
        #     [cell_borders[i][j] for j in range(1, self.W + 1)]
        #     for i in range(1, self.H + 1)
        # ]
        self.cells = self.__create_cells__(centers, cell_borders)

    def in_map(self, x, y):
        return 0 <= x < len(self.cells) and 0 <= y < len(self.cells[0])

    def image_size(self):
        if self.map_type == "VORONOI":
            return (self.W * self.size, self.H * self.size)
        elif self.map_type == "HEX":
            i = int(self.size * (self.H * 3 / 4 - 2))
            j = int(self.size * (self.W * sqrt(3) / 2 - 2))
            x = j
            y = i
            return (x, y)
        else:
            raise Exception("Incorrect map_type")

    def create_map(self):
        if self.map_type == "VORONOI":
            self.__generate_voronoi_map__()
        elif self.map_type == "HEX":
            self.__generate_hex_map__()

    def integrate_rivers(self):
        for i in range(len(self.rivers)):
            for j in range(i + 1, len(self.rivers)):
                river1 = self.rivers[i]
                river2 = self.rivers[j]
                if river1.intersect(river2):
                    river1.merge(river2)

        #for i in range(len(self.rivers)):
            #for (x, y) in self.rivers[i].path:
                #self.cells[x][y].river = True


    def rivers_finalize(self):

        self.integrate_rivers()

        for i in range(len(self.rivers)):
            for j in range(len(self.rivers[i].path)):
                (x, y) = self.rivers[i].path[j]
                self.cells[x][y].river = True

    
    def __distance__(self, point1, point2):
        (x1, y1) = point1
        (x2, y2) = point2
        (center_x1, center_y1) = self.cells[x1][y1].center
        (center_x2, center_y2) = self.cells[x2][y2].center
        dx, dy = abs(center_x2 - center_x1), abs(center_y2 - center_y1)
        return (dx ** 2 + dy ** 2) ** 0.5

    def create_roads(self, world_map, continent, terrains, bioms):
        self.terrains = terrains
        self.bioms = bioms
        cities = continent.cities
        radius = self.__calculate_connection__(cities)
        [all_connections, graph] = self.__create_graph__(cities, radius)
        self.all_road_endpoints += all_connections
        self.__find_odd_road_endpoints__(cities, graph)
        self.__remove_odd_road_endpoints__()
        self.__create_road_paths__(world_map, continent)


    def __calculate_connection__(self, cities):
        sum_distance = self.__sum_of_city_distances__(cities)
        N = len(cities) * (len(cities) - 1) / 2
        N = N * 2
        radius = sum_distance / N
        return radius

    def __create_graph__(self, cities, radius):
        graph = [ [0]*len(cities) for i in range(len(cities))]
        all_connections = []

        for i in range(len(cities)):
            for j in range(i+1, len(cities)):
                point1 = cities[i].points[0]
                point2 = cities[j].points[0]
                dist = self.__distance__(point1, point2)
                if dist <= radius:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    all_connections.append((cities[i], cities[j]))
        return [all_connections, graph]
        
    
    def __sum_of_city_distances__(self, cities):
        sum = 0
        for i in range(len(cities)):
            for j in range(i+1, len(cities)):
                point1 = cities[i].points[0]
                point2 = cities[j].points[0]
                sum += self.__distance__(point1, point2)
        return sum


    def __find_odd_road_endpoints__(self, cities, graph):
        odd_road_endpoints =[]
        for c1 in range(len(graph)):
            for c2 in range(c1+1, len(graph)):
                for c3 in range(c2+1, len(graph)):
                    if graph[c1][c2] == 0 or graph[c1][c3] == 0 or graph[c2][c3] == 0: 
                        continue

                    (city1, city2) = self.__check_triangle__(cities, c1, c2, c3)
                    if city1 == -1 and city2 == -1:
                        continue

                    odd_road_endpoints.append((cities[city1],cities[city2]))
                    graph[city1][city2] = 0

        self.odd_road_endpoints += odd_road_endpoints

    
    def __remove_odd_road_endpoints__(self):
        new_all_road_endpoints = []
        for road in self.all_road_endpoints:
            if not road in self.odd_road_endpoints:
                new_all_road_endpoints.append(road)
        self.all_road_endpoints = new_all_road_endpoints
        self.odd_road_endpoints = []

                    
        
    def __check_triangle__(self, cities, c1, c2, c3):
        triangles = [[c1,c2,c3],[c1,c3,c2],[c2,c1,c3],[c2,c3,c1],[c3,c1,c2],[c3,c2,c1]]
        for i in range(len(triangles)):
            city1 = triangles[i][0]
            city2 = triangles[i][1]
            city3 = triangles[i][2]
            
            (x1, y1) = cities[city1].points[0]
            (x2, y2) = cities[city2].points[0]
            (x3, y3) = cities[city3].points[0]

            point1 = self.cells[x1][y1].center
            point2 = self.cells[x2][y2].center
            point3 = self.cells[x3][y3].center

            vector1 = [point2[0] - point1[0], point2[1] - point1[1]]
            vector2 = [point3[0] - point2[0], point3[1] - point2[1]]

            cross_product = vector1[0]*vector2[1] - vector1[1]*vector2[0]  # sign is sign of sin
            dot_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]    # sign is sign of cos
            area = self.__distance__((x1, y1),(x2,y2)) * self.__distance__((x2, y2),(x3,y3))

            max_sin = 0.5
            sin = cross_product / area

            if dot_product >= 0 and sin > 0 and sin <= max_sin:
                print(cross_product, dot_product, area)
                odd = (triangles[i][0], triangles[i][2])
                print(odd)
                return odd

        return (-1, -1)


    def __create_road_paths__(self, world_map, continent):
        for i in range(len(self.all_road_endpoints)):
            road_endpoints = self.all_road_endpoints[i]
            road = Road(road_endpoints, world_map, continent, self.terrains, self.bioms)
            #print("endpoints", road_endpoints[0].points[0], road_endpoints[1].points[0])
            print("road", road.path)
            self.roads.append(road)

