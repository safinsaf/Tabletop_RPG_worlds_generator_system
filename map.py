import random
from math import sqrt

from scipy.spatial import Voronoi

from cell import Cell


class Map:

    H, W = 0, 0
    size = 0
    cells = []
    map_type = ""  # HEX|VORONOI
    # cells = [[Cell, Cell],[Cell, Cell]]

    def __init__(self, w=500, h=300, size=30, map_type="VORONOI"):
        self.W = w
        self.H = h
        self.size = size
        self.cells = []
        self.map_type = map_type

    def __grid__(self, i, j):
        if self.map_type == "VORONOI":
            return (
                self.size * (i + random.random()),
                self.size * (j + random.random()),
            )
        elif self.map_type == "HEX":
            if i % 2 == 0:
                x = self.size * (i / 2)
                y = self.size * j * sqrt(3)
                return (x, y)
            else:
                x = self.size * (i / 2)
                y = self.size * j * sqrt(3) + self.size * sqrt(3) / 2
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
        neigbors_even = [(2, 0), (-2, 0), (1, 0), (1, -1), (-1, 0), (-1, -1)]
        return neigbors_even

    def __hex_odd_neighbors__(self):
        neigbors_odd = [(2, 0), (-2, 0), (-1, 0), (1, 0), (-1, 1), (1, 1)]
        return neigbors_odd

    def __find_neighbors__(self, area_object):
        neighbors = []
        for el in area_object.coords_arr:
            d = []
            if self.map_type == "VORONOI":
                d = self.__voronoi_neighbors__()
            elif self.map_type == "HEX":
                if el[0] % 2 == 0:
                    d = self.__hex_odd_neighbors__()
                elif el[0] % 2 == 1:
                    d = self.__hex_even_neighbors__()
            possible_neighbors = []
            for (dx, dy) in d:
                possible_neighbors.append((el[0] + dx, el[1] + dy))
            for (x, y) in possible_neighbors:
                if area_object.__free__(x, y, self):
                    neighbors.append((x, y))
        return neighbors

    def __create_voronoi__(self, centers):

        centers_merged = []
        for i in range(self.H + 2):
            for j in range(self.W + 2):
                centers_merged.append(centers[i][j])
        voronoi = Voronoi(centers_merged)

        vertices = voronoi.vertices
        regions = voronoi.regions
        point_region = voronoi.point_region

        cell_regions = [[[] for j in range(self.W)] for i in range(self.H)]

        for row in range(1, self.H + 1):
            for col in range(1, self.W + 1):
                cur_ind = point_region[row * (self.W + 2) + col]
                cur_reg = regions[cur_ind]
                for el in cur_reg:

                    point = vertices[el]
                    point = tuple(point)
                    # point = (point[1], point[0])
                    cell_regions[row - 1][col - 1].append(point)

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
        centers = [
            [self.__grid__(i - 1, j - 1) for j in range(self.W + 2)]
            for i in range(self.H + 2)
        ]

        cell_borders = self.__create_voronoi__(centers)

        centers = [
            [centers[i][j] for j in range(1, self.W + 1)] for i in range(1, self.H + 1)
        ]

        self.cells = self.__create_cells__(centers, cell_borders)

    def __generate_hex_map__(self):
        centers = [
            [self.__grid__(i - 1, j - 1) for j in range(self.W + 2)]
            for i in range(self.H + 2)
        ]

        cell_borders = []
        for i in range(self.H + 2):
            cell_borders.append([])
            for j in range(self.W + 2):
                cur_center = centers[i][j]
                a = 1 / 2
                b = 1 / (2 * sqrt(3))

                d = [(a, b), (0, 2 * b), (-a, b), (-a, -b), (0, -2 * b), (a, -b)]

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

        centers = [
            [centers[i][j] for j in range(1, self.W + 1)] for i in range(1, self.H + 1)
        ]
        self.cells = self.__create_cells__(centers, cell_borders)

    def in_map(self, x, y):
        return 0 <= x < len(self.cells) and 0 <= y < len(self.cells[0])

    def image_size(self):
        if self.map_type == "VORONOI":
            return (self.W * self.size, self.H * self.size)
        elif self.map_type == "HEX":
            i = self.size * self.H // 2
            j = int(self.size * self.W * sqrt(3))
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
