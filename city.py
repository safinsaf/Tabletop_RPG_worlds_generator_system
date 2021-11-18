import random


class City:
    def __init__(self, name, continent, world_map):
        self.name = name
        points = continent.coords_arr
        random.shuffle(points)
        for (x1, y1) in points:
            if not world_map.cells[x1][y1].river:
                continue
            if world_map.cells[x1][y1].city != "NoCity":
                continue
            height = world_map.cells[x1][y1].height
            neighbors = world_map.__find_all_neighbors__([(x1, y1)])
            random.shuffle(neighbors)
            area = [(x1, y1)]
            for (x2, y2) in neighbors:
                if world_map.cells[x2][y2].city != "NoCity":
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
            if world_map.cells[x][y].city == "NoCity":
                world_map.cells[x][y].city = self.name + "Suburb"
