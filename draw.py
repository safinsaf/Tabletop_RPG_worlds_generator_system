from datetime import datetime

from PIL import Image, ImageDraw
from map import Map



def draw_map(world_map: Map, map_name: str, rivers = True, cities = True, roads = True):
    image_size = world_map.image_size()
    img = Image.new("RGB", (image_size[0], image_size[1]))
    draw = ImageDraw.Draw(img, "RGBA")

    for i in range(world_map.H):
        for j in range(world_map.W):
            draw.polygon(
                [(y, x) for (x, y) in world_map.cells[i][j].borders],
                fill=world_map.cells[i][j].color
            )
            if world_map.cells[i][j].border_color != (-1, -1, -1, -1):
                polygon = world_map.cells[i][j].borders
                polygon.append(world_map.cells[i][j].borders[0])
                draw.line(
                    [(y, x) for (x, y) in polygon],
                    fill=world_map.cells[i][j].border_color,
                    width=10
                )
            (x, y) = world_map.cells[i][j].center
            draw.text((y - 10, x - 10), str(world_map.cells[i][j].height))
            draw.text((y - 10, x), "%s %s" % (int(i), int(j)))
            #draw.text((y - 10, x + 10), "%s" % world_map.cells[i][j].level_0)
            #draw.text((y - 10, x + 20), "%s" % world_map.cells[i][j].level_1)

    if rivers:
        for river_obj in world_map.rivers:
            river = river_obj.path
            if len(river) == 0:
                continue
            for i in range(0, len(river) - 1):
                current = river[i]
                next = river[i + 1]
                x1, y1 = current[0], current[1]
                x2, y2 = next[0], next[1]
                (x1_center, y1_center) = world_map.cells[x1][y1].center
                (x2_center, y2_center) = world_map.cells[x2][y2].center
                draw.line(
                    (y1_center, x1_center, y2_center, x2_center),
                    fill=(100, 100, 100),
                    width=world_map.size // 10,
                )

    if cities:
        for city_obj in world_map.cities:
            city_points = city_obj.points
            for (x, y) in city_points:
                (x_center, y_center) = world_map.cells[x][y].center
                draw.rectangle(
                    (y_center - 10, x_center - 10, y_center + 10, x_center + 10),
                    fill=(255, 0, 0),
                )
            if city_obj.port:
                (port_x, port_y) = city_obj.port
                (port_x_center, port_y_center) = world_map.cells[port_x][port_y].center
                draw.rectangle(
                    (port_y_center - 5, port_x_center - 5, port_y_center + 5, port_x_center + 5),
                    fill=(0, 0, 255),
                )

    # for i in range(len(world_map.all_road_endpoints)):
    #     (city1, city2) = world_map.all_road_endpoints[i]
    #     x1 = city1.points[0][0]
    #     y1 = city1.points[0][1]
    #     x2 = city2.points[0][0]
    #     y2 = city2.points[0][1]

    #     points = [world_map.cells[x1][y1].center, world_map.cells[x2][y2].center]
    #     draw.line(
    #             [(y, x) for (x, y) in points],
    #             fill=(255,255,255),
    #             width=5
    #             )

    # for i in range(len(world_map.odd_road_endpoints)):
    #     (city1, city2) = world_map.odd_road_endpoints[i]
    #     x1 = city1.points[0][0]
    #     y1 = city1.points[0][1]
    #     x2 = city2.points[0][0]
    #     y2 = city2.points[0][1]

    #     points = [world_map.cells[x1][y1].center, world_map.cells[x2][y2].center]
    #     draw.line(
    #             [(y, x) for (x, y) in points],
    #             fill=(255,0,0),
    #             width=5
    #             )

    if roads:
        for road_obj in world_map.roads:
            road = road_obj.path
            #print(road)
            if len(road) == 0:
                continue
            for i in range(0, len(road) - 1):
                current = road[i]
                next = road[i + 1]
                x1, y1 = current[0], current[1]
                x2, y2 = next[0], next[1]
                (x1_center, y1_center) = world_map.cells[x1][y1].center
                (x2_center, y2_center) = world_map.cells[x2][y2].center
                draw.line(
                    (y1_center, x1_center, y2_center, x2_center),
                    fill=(200, 0, 0),
                    width=5,    
                    )

    time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    img.save("images/" + time + "_" + map_name, "PNG")