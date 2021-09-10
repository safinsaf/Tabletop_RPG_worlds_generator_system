from PIL import Image, ImageDraw

from continent import Continent
from map import Map
from terrain import Terrain
from terrains.__read_terrains__ import read_terrains

# HEIGHT, WIDTH = 100, 200
# MAP_TYPE = "VORONOI"  # HEX|VORONOI

HEIGHT, WIDTH = 50, 25
MAP_TYPE = "HEX"  # HEX|VORONOI

size = 100

worldMap = Map(WIDTH, HEIGHT, size, MAP_TYPE)


# VORONOI
# continent1 = Continent((50, 50), "Asia")
# continent2 = Continent((30, 150), "Europe")
# continent3 = Continent((70, 100), "America")
# for i in range(150):
#     continent1.increase_territory(worldMap, 10)
#     continent2.increase_territory(worldMap, 10)
#     continent3.increase_territory(worldMap, 5)
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

continent1 = Continent((25, 12), "Asia", worldMap)
# continent2 = Continent((150, 150), "Europe")
# continent3 = Continent((100, 100), "America")
for i in range(15):
    continent1.increase_territory(worldMap, 10)
    # continent2.increase_territory(worldMap, 10)
    # continent3.increase_territory(worldMap, 5)

terrains = read_terrains()

terrain1 = Terrain((25, 12), "A", "Plain", worldMap, terrains)
# terrain2 = Terrain((104, 50), "B", "Mountain", worldMap, terrains)
# terrain3 = Terrain((97, 52), "C", "Hill", worldMap, terrains)
# terrain4 = Terrain((110, 55), "D", "Mountain", worldMap, terrains)
# terrain5 = Terrain((105, 45), "E", "Plain", worldMap, terrains)
# terrain6 = Terrain((95, 45), "F", "Mountain", worldMap, terrains)
# terrain7 = Terrain((100, 51), "G", "Hill", worldMap, terrains)

for i in range(20):
    terrain1.increase_territory(worldMap, 10)
    # terrain2.increase_territory(worldMap, 10)
    # terrain3.increase_territory(worldMap, 10)
    # terrain4.increase_territory(worldMap, 10)
    # terrain5.increase_territory(worldMap, 10)
    # terrain6.increase_territory(worldMap, 10)
    # terrain7.increase_territory(worldMap, 10)

terrain1.set_height(worldMap)
# terrain2.set_height(worldMap)
# terrain3.set_height(worldMap)
# terrain4.set_height(worldMap)
# terrain5.set_height(worldMap)
# terrain6.set_height(worldMap)
# terrain7.set_height(worldMap)


# bioms = read_bioms()

# biom1 = Biom((100, 45), "Forest A", "Forest", bioms)
# biom2 = Biom((150, 145), "Swamp B", "Swamp", bioms)
# biom3 = Biom((95, 100), "Desert C", "Desert", bioms)
# biom4 = Biom((95, 50), "Tundra A", "Tundra", bioms)
# biom5 = Biom((145, 150), "Mountain B", "Mountain", bioms)
# biom6 = Biom((100, 105), "Hill C", "Hill", bioms)
# biom7 = Biom((100, 55), "Mountain C", "Mountain", bioms)


# for i in range(100):
#     biom1.increase_territory(worldMap, 10)
#     biom2.increase_territory(worldMap, 10)
#     biom3.increase_territory(worldMap, 5)
#     biom4.increase_territory(worldMap, 10)
#     biom5.increase_territory(worldMap, 10)
#     biom6.increase_territory(worldMap, 10)
#     biom7.increase_territory(worldMap, 10)

image_size = worldMap.image_size()
img = Image.new("RGB", (image_size[0], image_size[1]))
draw = ImageDraw.Draw(img, "RGBA")


for i in range(HEIGHT):
    for j in range(WIDTH):
        draw.polygon(
            [(y, x) for (x, y) in worldMap.cells[i][j].borders],
            fill=worldMap.cells[i][j].color,
        )
        (x, y) = worldMap.cells[i][j].center
        draw.text((y - 10, x - 10), str(worldMap.cells[i][j].height))
        draw.text((y - 10, x), "%s %s" % (int(i), int(j)))
        draw.text((y - 10, x + 10), "%s" % worldMap.cells[i][j].level_0)
        draw.text((y - 10, x + 20), "%s" % worldMap.cells[i][j].level_1)

print(continent1.coords_arr)
img.save(r"map.png", "PNG")
