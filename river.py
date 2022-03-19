import random


class River:

    path = []

    def __init__(self, world_map, continent):
        mountains = self.__find_all_sources__(continent, world_map)
        coasts = self.__find_all_coasts__(continent, world_map)
        while True:
            mountain = mountains[random.randint(0, len(mountains) - 1)]
            coast = coasts[random.randint(0, len(coasts) - 1)]

            path = self.__try_find_path__(coast, mountain, world_map, continent)
            if path:
                break
        
        #connect to the Ocean
        neighbors = world_map.__find_all_neighbors__([coast])
        neighbor_ocean = 0
        for (i, j) in neighbors:
            if world_map.cells[i][j].level_0 == "Ocean":
                neighbor_ocean = (i, j)
                break
        path = [neighbor_ocean] + path
        self.path = path


    def __next_point__(self, current_point, final_point, world_map):

        neighbors = world_map.__find_all_neighbors__([(current_point)])
        right_neighbors = []

        (x1, y1) = current_point
        (xf, yf) = final_point
        (center_x1, center_y1) = world_map.cells[x1][y1].center
        (center_xf, center_yf) = world_map.cells[xf][yf].center
        dx1, dy1 = abs(center_xf - center_x1), abs(center_yf - center_y1)
        for (x2, y2) in neighbors:
            (center_x2, center_y2) = world_map.cells[x2][y2].center
            dx2, dy2 = abs(center_xf - center_x2), abs(center_yf - center_y2)
            if world_map.cells[x2][y2].level_0 == "Ocean":
                continue
            if (
                dx1 ** 2 + dy1 ** 2 >= dx2 ** 2 + dy2 ** 2
                and world_map.cells[x2][y2].height >= world_map.cells[x1][y1].height
            ):
                right_neighbors.append((x2, y2))
        if len(right_neighbors) == 0:
            print("Could not create a river, try again")
            return None
        next_point = right_neighbors[random.randint(0, len(right_neighbors) - 1)]
        return next_point


    def __find_all_coasts__(self, continent, world_map):
        coasts = []
        for (x, y) in continent.coords_arr:
            neighbors = world_map.__find_all_neighbors__([(x, y)])
            is_edge = any(
                world_map.cells[i][j].level_0 == "Ocean" for (i, j) in neighbors
            )
            if not is_edge:
                continue
            coasts.append((x, y))
        return coasts

    def __find_all_sources__(self, continent, world_map):
        max_height = 0
        all_points = continent.coords_arr
        for (x, y) in all_points:
            if world_map.cells[x][y].height > max_height:
                max_height = world_map.cells[x][y].height

        possible_sources = []
        for (x, y) in all_points:
            if world_map.cells[x][y].height >= max_height - 3:
                possible_sources.append((x, y))
        return possible_sources

    def __find_intersecting_points__(self, other_river):
        path1 = self.path
        path2 = other_river.path
        set_path_1 = set(path1)
        intersections = [point for point in path2 if point in set_path_1]
        return intersections

    def intersect(self, other_river):
        intersections = self.__find_intersecting_points__(other_river)
        if len(intersections) > 0:
            return True
        return False

    def merge(self, other_river):
        if other_river == self:
            return True
        intersections = self.__find_intersecting_points__(other_river)
        if len(intersections) == 0:
            return False
        merge_point = intersections[-1]
        other_river.path = other_river.path[other_river.path.index(merge_point) :]
        return True

    def __try_find_path__(self, coast, mountain, world_map, continent):
        vertices = continent.coords_arr
        vertices_inverse = {}
        for i in range(len(vertices)):
            vertices_inverse[vertices[i]] = i
        edges = [[] for i in range(len(vertices))]

        for i in range(len(vertices)):
            neighbors_i = world_map.__find_all_neighbors__([vertices[i]])
            for j in range(len(neighbors_i)):
                (x, y) = neighbors_i[j]
                if world_map.cells[x][y].level_0 == "Ocean":
                    continue
                index = vertices_inverse[neighbors_i[j]]
                edges[i].append(index)
                edges[index].append(i)

        point = coast
        vertex = vertices_inverse[point]
        visited = [-1] * len(vertices)

        path = [vertex]
        visited[vertex] = 1
        while len(path) > 0:
            current = path[-1]
            if vertices[current] == mountain:
                path_vertices = []
                for i in range(len(path)):
                    path_vertices.append(vertices[path[i]])
                return path_vertices
            for i in range(len(edges[current])):
                neighbor = edges[current][i]
                distance1 = self.__distance__(vertices[current], mountain, world_map)
                distance2 = self.__distance__(vertices[neighbor], mountain, world_map)

                (x1, y1) = vertices[current]
                (x2, y2) = vertices[neighbor]
                if not (
                    distance1 >= distance2
                    and world_map.cells[x2][y2].height >= world_map.cells[x1][y1].height
                ):
                    continue

                if visited[neighbor] == -1:
                    path.append(neighbor)
                    visited[neighbor] = 1
                    break
            else:
                path.pop()
        # no path
        return []

    def __distance__(self, point1, point2, world_map):
        (x1, y1) = point1
        (x2, y2) = point2
        (center_x1, center_y1) = world_map.cells[x1][y1].center
        (center_x2, center_y2) = world_map.cells[x2][y2].center
        dx, dy = abs(center_x2 - center_x1), abs(center_y2 - center_y1)
        return dx ** 2 + dy ** 2