from PIL import Image, ImageDraw

from biom import Biom
from continent import Continent
from map import Map
from plugins.__read_bioms__ import read_bioms

H, W = 100, 200
size = 100

img = Image.new("RGB", (W * size, H * size))
draw = ImageDraw.Draw(img, "RGBA")

worldMap = Map(W, H, size)
worldMap.create_map()


continent1 = Continent((50, 50), "Asia")
continent2 = Continent((30, 150), "Europe")
continent3 = Continent((70, 100), "America")
for i in range(150):
    continent1.increase_territory(worldMap, 10)
    continent2.increase_territory(worldMap, 10)
    continent3.increase_territory(worldMap, 5)

bioms = read_bioms()


biom1 = Biom((45, 45), "Forest A", "Forest", bioms)
biom2 = Biom((30, 150), "Swamp B", "Swamp", bioms)
biom3 = Biom((70, 100), "Desert C", "Desert", bioms)
biom4 = Biom((55, 55), "Tundra A", "Tundra", bioms)
biom5 = Biom((20, 140), "Mountain B", "Mountain", bioms)
biom6 = Biom((65, 105), "Hill C", "Hill", bioms)
biom7 = Biom((60, 65), "Mountain C", "Mountain", bioms)

for i in range(100):
    biom1.increase_territory(worldMap, 10)
    biom2.increase_territory(worldMap, 10)
    biom3.increase_territory(worldMap, 5)
    biom4.increase_territory(worldMap, 10)
    biom5.increase_territory(worldMap, 10)
    biom6.increase_territory(worldMap, 10)
    biom7.increase_territory(worldMap, 10)


for i in range(H):
    for j in range(W):
        draw.polygon(worldMap.cells[i][j].borders, fill=worldMap.cells[i][j].color)

img.save(r"map.png", "PNG")
