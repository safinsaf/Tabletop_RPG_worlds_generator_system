from time import sleep


class CoordsFinder():
    def find_coords(self, area_object, world_map, matrix, entities_count):
        up_count = 0
        down_count = 0
        left_count = 0
        right_count = 0

        point_indexes = area_object.all_cell_indexes()
        point_coords = area_object.all_cell_coords(world_map)

        up_initial = 1e10
        down_initial = 0
        left_initial = 1e10
        right_initial = 0
        for i in range(len(point_coords)):
            if point_coords[i][0] < up_initial:
                up_initial = point_coords[i][0]
            if point_coords[i][0] > down_initial:
                down_initial = point_coords[i][0]
            if point_coords[i][1] < left_initial:
                left_initial = point_coords[i][1]
            if point_coords[i][1] > right_initial:
                right_initial = point_coords[i][1]
        
        step = world_map.size

        while True:

            up = up_initial + step * up_count
            down = down_initial - step * down_count
            left = left_initial + step * left_count
            right = right_initial - step * right_count
            
            borders = [left, right, up, down]

            #print(borders)

            coordinates = self.change_size(borders, matrix)

            #print(coordinates)


            coords = [0 for i in range(len(entities_count))]

            for i in range(len(entities_count)):
                x, y = coordinates[i]
                
                found_place = False
                for j in range(len(point_coords)):
                    if self.in_square((x, y), point_coords[j], world_map.size):
                        found_place = True
                        coords[i] = point_indexes[j]
                #print(i, found_place)
                
                if not found_place:
                    # a = self.find_closest_point((x, y), point_coords)
                    # print(a)
                    # coords[i] = point_indexes[a[2]]
                    # continue

                    # closest_border = self.closest_border((x, y), borders)
                    # left_count = left_count + 1 if closest_border == "left" else left_count
                    # right_count = right_count + 1 if closest_border == "right" else right_count
                    # up_count = up_count + 1 if closest_border == "up" else up_count
                    # down_count = down_count + 1 if closest_border == "down" else down_count

                    left_count = left_count + 1 
                    right_count = right_count + 1
                    up_count = up_count + 1 
                    down_count = down_count + 1 

                    break
            else:
                return coords

    def find_closest_point(self, coords, points):
        distance = 1e20
        closest_coords = (-1, -1)
        for i in range(len(points)):
            d = ((coords[0]-points[i][0])**2 + (coords[1]-points[i][1])**2) ** 0.5
            if d < distance:
                distance = d
                closest_coords = points[i]
        return (distance, closest_coords, i)

    def change_size(self, borders, matrix):
        left = borders[0]
        right = borders[1]
        up = borders[2]
        down = borders[3]
        coordinates = {}
        part_x = (down - up) / (len(matrix[0])+1)
        part_y = (right - left) / (len(matrix)+1)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                x = up + part_x + (i) * part_x
                y = left + part_y + (j) * part_y
                if matrix[i][j] >= 0:
                    coordinates[matrix[i][j]] = (x, y)
        return coordinates


    def in_square(self, coord, center, radius):
        
        x, y = coord[0], coord[1]
        x_center, y_center = center[0], center[1]
        is_x = x_center - radius <= x <= x_center + radius
        is_y = y_center - radius <= y <= y_center + radius
        #print("x", x_center - radius, x, x_center + radius)
        #print("y", y_center - radius, y, y_center + radius)
        if is_x and is_y:
            return True
        return False

    def closest_border(self, coord, borders):
        left = borders[0]
        right = borders[1]
        up = borders[2]
        down = borders[3]

        d_l = abs(left - coord[1])
        d_r = abs(right - coord[1])
        d_u = abs(up - coord[0])
        d_d = abs(down - coord[0])

        if d_l <= d_r and d_l <= d_u and d_l <= d_d:
            return "left"
        elif d_r <= d_u and d_r <= d_d:
            return "right"
        elif d_u <= d_d:
            return "up"
        else: 
            return "down"
