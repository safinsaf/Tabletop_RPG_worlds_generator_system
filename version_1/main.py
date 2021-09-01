from PIL import Image, ImageDraw
import random
from map import Map
from continent import Continent
from scipy.spatial import Voronoi
import time

H, W = 100, 200
size = 100

img = Image.new("RGB", (W*size, H*size))
draw = ImageDraw.Draw(img, "RGBA")

worldMap = Map(W, H, size)
worldMap.create_map()


continent1 = Continent((50, 50), "Asia")
continent2 = Continent((30, 150), "Europe")
continent3 = Continent((70, 100), "America")
for i in range(150):
	continent1.increase_territory(worldMap, 5)
	continent2.increase_territory(worldMap, 5)
	continent3.increase_territory(worldMap, 5)



for i in range(H):
	for j in range(W):
		draw.polygon(worldMap.cells[i][j].borders, fill = worldMap.cells[i][j].color)

img.save("map.png")

