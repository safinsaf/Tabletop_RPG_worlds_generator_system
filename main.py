from PIL import Image, ImageDraw

from biom import Biom
from continent import Continent
from map import Map
from plugins.__read_bioms__ import read_bioms

# HEIGHT, WIDTH = 100, 200
# MAP_TYPE = "VORONOI"  # HEX|VORONOI

HEIGHT, WIDTH = 300, 200
MAP_TYPE = "HEX"  # HEX|VORONOI

size = 100

worldMap = Map(WIDTH, HEIGHT, size, MAP_TYPE)
worldMap.create_map()

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

continent1 = Continent((100, 50), "Asia")
continent2 = Continent((150, 150), "Europe")
continent3 = Continent((100, 100), "America")
for i in range(150):
    continent1.increase_territory(worldMap, 10)
    continent2.increase_territory(worldMap, 10)
    continent3.increase_territory(worldMap, 5)

bioms = read_bioms()


biom1 = Biom((100, 45), "Forest A", "Forest", bioms)
biom2 = Biom((150, 145), "Swamp B", "Swamp", bioms)
biom3 = Biom((95, 100), "Desert C", "Desert", bioms)
biom4 = Biom((95, 50), "Tundra A", "Tundra", bioms)
biom5 = Biom((145, 150), "Mountain B", "Mountain", bioms)
biom6 = Biom((100, 105), "Hill C", "Hill", bioms)
biom7 = Biom((100, 55), "Mountain C", "Mountain", bioms)


for i in range(100):
    biom1.increase_territory(worldMap, 10)
    biom2.increase_territory(worldMap, 10)
    biom3.increase_territory(worldMap, 5)
    biom4.increase_territory(worldMap, 10)
    biom5.increase_territory(worldMap, 10)
    biom6.increase_territory(worldMap, 10)
    biom7.increase_territory(worldMap, 10)

image_size = worldMap.image_size()
img = Image.new("RGB", (image_size[0], image_size[1]))
draw = ImageDraw.Draw(img, "RGBA")


for i in range(HEIGHT):
    for j in range(WIDTH):
        draw.polygon(
            [(y, x) for (x, y) in worldMap.cells[i][j].borders],
            fill=worldMap.cells[i][j].color,
        )

img.save(r"map.png", "PNG")
