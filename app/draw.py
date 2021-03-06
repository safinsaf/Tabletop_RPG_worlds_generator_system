from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from numpy import size
from app.map import Map
import os

class Drawer():

    def __init__(self):
        parent_dir = "all_outputs/"
        directory = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        self.folder = path
        

    def draw_map(self, world_map: Map, map_name: str, rivers = True, cities = True, roads = True):
        image_size = world_map.image_size()
        img = Image.new("RGB", (image_size[0], image_size[1]))
        draw = ImageDraw.Draw(img, "RGBA")

        for i in range(world_map.H):
            for j in range(world_map.W):
                draw.polygon(
                    [(y, x) for (x, y) in world_map.cells[i][j].borders],
                    fill=world_map.cells[i][j].color
                )
                # if world_map.cells[i][j].border_color != (-1, -1, -1, -1):
                #     polygon = world_map.cells[i][j].borders
                #     polygon.append(world_map.cells[i][j].borders[0])
                #     draw.line(
                #         [(y, x) for (x, y) in polygon],
                #         fill=world_map.cells[i][j].border_color,
                #         width=world_map.size//3
                #     )
                draw.polygon(
                    [(y, x) for (x, y) in world_map.cells[i][j].borders],
                    fill=world_map.cells[i][j].border_color
                )
                (x, y) = world_map.cells[i][j].center
                draw.text((y - 10, x - 20), str(world_map.cells[i][j].height))
                draw.text((y - 10, x - 10), "%s %s" % (int(i), int(j)))
                draw.text((y - 10, x), "%s" % world_map.cells[i][j].level_0)
                draw.text((y - 10, x + 10), "%s" % world_map.cells[i][j].level_1)
                draw.text((y - 10, x + 20), "%s" % world_map.cells[i][j].level_2)

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
                        fill=(0, 0, 255),
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

        img.save(os.path.join(self.folder, map_name + ".png"), "PNG")



    def draw_schema(self, schema_name, names, schema):
        image_size = 300
        font_file = "fonts/GrandHotel-Regular.otf"
        font = ImageFont.truetype(font_file, 30)
        fontheader = ImageFont.truetype(font_file, 60)
        ss = 30

        if len(schema) == 0:
            print("Nothing to draw for" + schema_name)
            return

        img = Image.new("RGB", ((len(schema[0])+1)*image_size, (len(schema)+1)*image_size), (200,200,200))
        draw = ImageDraw.Draw(img, "RGBA")

        draw.text((10, 10), "%s" % (schema_name), fill=(0,0,0), font=fontheader)
        
        for i in range(len(schema)):
            for j in range(len(schema[0])):
                x_center = (i+1) * image_size
                y_center = (j+1) * image_size
                if schema[i][j] == -1:
                    continue
                draw.rectangle(
                    (y_center - ss, x_center - ss, y_center + ss, x_center + ss),
                    fill=(255, 0, 0),
                )
                draw.text((y_center - ss, x_center - 2*ss), names[schema[i][j]], fill=(0,0,0), font=font) 

        
        img.save(os.path.join(self.folder, schema_name + ".png"), "PNG")
