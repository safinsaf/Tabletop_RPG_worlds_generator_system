from datetime import datetime

from PIL import Image, ImageDraw

from city import City
from continent import Continent
from map import Map
from river import River
from terrain import Terrain
from biom import Biom
from terrains.__read_terrains__ import read_terrains
from plugins.__read_bioms__ import read_bioms
from races.__read_races__ import read_races

# HEIGHT, WIDTH = 100, 200
# MAP_TYPE = "VORONOI"  # HEX|VORONOI

HEIGHT, WIDTH = 80, 100
MAP_TYPE = "HEX"  # HEX|VORONOI

size = 50

world_map = Map(WIDTH, HEIGHT, size, MAP_TYPE)


def draw_map(map_name):
    image_size = world_map.image_size()
    img = Image.new("RGB", (image_size[0], image_size[1]))
    draw = ImageDraw.Draw(img, "RGBA")

    for i in range(HEIGHT):
        for j in range(WIDTH):
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
                width=size // 10,
            )

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

    for i in range(len(world_map.all_road_endpoints)):
        (city1, city2) = world_map.all_road_endpoints[i]
        x1 = city1.points[0][0]
        y1 = city1.points[0][1]
        x2 = city2.points[0][0]
        y2 = city2.points[0][1]

        points = [world_map.cells[x1][y1].center, world_map.cells[x2][y2].center]
        draw.line(
                [(y, x) for (x, y) in points],
                fill=(255,255,255),
                width=5
                )

    # for i in range(len(world_map.odd_roads)):
    #     (city1, city2) = world_map.odd_roads[i]
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


# VORONOI
# continent1 = Continent((50, 50), "Asia")
# continent2 = Continent((30, 150), "Europe")
# continent3 = Continent((70, 100), "America")
# for i in range(150):
#     continent1.increase_territory(world_map, 10)
#     continent2.increase_territory(world_map, 10)
#     continent3.increase_territory(world_map, 5)
#
# bioms = read_bioms()
#
#
# biom1 = Biom((45, 45), "Forest A", "Forest", bioms)
# biom2 = Biom((30, 150), "Swamp B", "Swamp", bioms)
# biom3 = Biom((70, 100), "Desert C", "Desert", bioms)
# biom4 = Biom((55, 55), "Tundra A", "Tundra", bioms)
# biom5 = Biom((20, 140), "Mountain B", "Mountain", bioms)
# biom6 = Biom((65, 105), "Hill C", "Hill", bioms)
# biom7 = Biom((60, 65), "Mountain C", "Mountain", bioms)

# HEX

continent1 = Continent((40, 50), "Asia", world_map)
# continent2 = Continent((150, 150), "Europe")
# continent3 = Continent((100, 100), "America")
for i in range(250):
    continent1.increase_territory(world_map, 10)
    # continent2.increase_territory(world_map, 10)
    # continent3.increase_territory(world_map, 5)

draw_map("before.png")

continent1.fill_holes(world_map)

terrains = read_terrains()

terrain1 = Terrain((45, 54), "A", "Plain", world_map, terrains)
terrain2 = Terrain((50, 45), "B", "Mountain", world_map, terrains)
terrain3 = Terrain((40, 45), "C", "Hill", world_map, terrains)
# terrain4 = Terrain((110, 55), "D", "Mountain", world_map, terrains)
# terrain5 = Terrain((105, 45), "E", "Plain", world_map, terrains)
# terrain6 = Terrain((95, 45), "F", "Mountain", world_map, terrains)
# terrain7 = Terrain((100, 51), "G", "Hill", world_map, terrains)

for i in range(150):
    terrain1.increase_territory(world_map, 10)
    terrain2.increase_territory(world_map, 10)
    terrain3.increase_territory(world_map, 10)
    # terrain4.increase_territory(world_map, 10)
    # terrain5.increase_territory(world_map, 10)
    # terrain6.increase_territory(world_map, 10)
    # terrain7.increase_territory(world_map, 10)

terrain1.set_height(world_map)
terrain2.set_height(world_map)
terrain3.set_height(world_map)
# terrain4.set_height(world_map)
# terrain5.set_height(world_map)
# terrain6.set_height(world_map)
# terrain7.set_height(world_map)

for i in range(40):
    river = River(world_map, continent1)
    world_map.rivers.append(river)
#
# for i in range(len(world_map.rivers)):
#      for j in range(i+1, len(world_map.rivers)):
#          river1 = world_map.rivers[i]
#          river2 = world_map.rivers[j]
#          if river1.intersect(river2):
#              river1.merge(river2)

world_map.rivers_finalize()


races = read_races()

cities = []
for i in range(20):
    city = City("city" + str(i), continent1, world_map, races, "Human")
    cities.append(city)
world_map.cities = cities


draw_map("after.png")

bioms = read_bioms()

biom1 = Biom((45, 45), "Forest A", "Forest", bioms)
biom2 = Biom((50, 60), "Swamp B", "Swamp", bioms)
biom3 = Biom((55, 55), "Desert C", "Desert", bioms)
biom4 = Biom((60, 35), "Tundra A", "Tundra", bioms)

print(dir(world_map.cells[45][45]))

for i in range(100):
    biom1.increase_territory(world_map, 10)
    biom2.increase_territory(world_map, 10)
    biom3.increase_territory(world_map, 5)
    biom4.increase_territory(world_map, 10)


world_map.create_roads(world_map, continent1, terrains, bioms)


draw_map("bioms.png")