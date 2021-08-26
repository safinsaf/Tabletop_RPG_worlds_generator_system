from PIL import Image, ImageDraw
import random
from scipy.spatial import Voronoi
import time

H, W = 300, 500
size = 30

def grid(size, i, j):
	return (size*(i + random.random()), size*(j + random.random()))

arr = [[grid(size, i, j) for j in range(W)] for i in range(H)]

img = Image.new("RGB", (W*size, H*size))
draw = ImageDraw.Draw(img, "RGBA")

for i in range(H):
	for j in range(W):
		draw.point((arr[i][j][1], arr[i][j][0]))

q = []
for i in range(H):
	for j in range(W):
		q.append(arr[i][j])
vor = Voronoi(q)

ver = vor.vertices
reg = vor.regions
point_reg = vor.point_region

arr2 = [[[] for j in range(W)] for i in range(H)]

for i in range(H):
	for j in range(W):
		cur_ind = point_reg[i*W + j]
		cur_reg = reg[cur_ind]
		for z in range(len(cur_reg)):
			if cur_reg[z] == -1:
				continue

			p = ver[cur_reg[z]]
			p = tuple(p)
			point = (p[1], p[0])
			arr2[i][j].append(point)

arr3 = [[[] for j in range(W)] for i in range(H)]

for i in range(H):
	for j in range(W):
		R = random.randint(0, 10)
		G = random.randint(0, 10)
		B = random.randint(245, 255)
		T = random.randint(100, 102)
		draw.polygon(arr2[i][j], fill=(R, G, B, T))

img.save("map.png")


## Create continents

