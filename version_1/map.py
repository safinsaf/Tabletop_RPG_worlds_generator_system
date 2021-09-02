import random
from scipy.spatial import Voronoi
from cell import Cell

class Map:

    H, W = 0, 0
    size = 0
    cells = []
    # cells = [[Cell, Cell],[Cell, Cell]]

    def __init__(self, w = 500, h = 300, size = 30):
        self.W = w
        self.H = h
        self.size = size
        self.cells = []

    def __grid__(self, size, i, j):
        return (self.size * (i + random.random()), self.size*(j + random.random()))

    def __create_voronoi__(self, centers):

        centers_merged = []
        for i in range(self.H+2):
            for j in range(self.W+2):
                centers_merged.append(centers[i][j])
        voronoi = Voronoi(centers_merged)

        vertices = voronoi.vertices
        regions = voronoi.regions
        point_region = voronoi.point_region

        cell_regions = [[[] for j in range(self.W)] for i in range(self.H)]

        for row in range(1, self.H+1):
            for col in range(1, self.W+1):
                cur_ind = point_region[row*(self.W+2) + col]
                cur_reg = regions[cur_ind]
                for z in range(len(cur_reg)):
                    if cur_reg[z] == -1:
                        continue

                    point = vertices[cur_reg[z]]
                    point = tuple(point)
                    point = (point[1], point[0])
                    cell_regions[row-1][col-1].append(point)

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
        centers = [[self.__grid__(self.size, i-1, j-1) for j in range(self.W+2)] for i in range(self.H+2)]

        cell_borders = self.__create_voronoi__(centers)

        centers = [[centers[i][j] for j in range(1, self.W+1)] for i in range(1, self.H + 1)]

        self.cells = self.__create_cells__(centers, cell_borders)


    def create_map(self):

        self.__generate_voronoi_map__()



