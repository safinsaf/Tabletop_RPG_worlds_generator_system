from city import City
from continent import Continent
from map import Map
from river import River
from terrain import Terrain
from biom import Biom
from terrains.__read_terrains__ import read_terrains
from plugins.__read_bioms__ import read_bioms
from races.__read_races__ import read_races
from draw import draw_map, draw_schema

from inputs.read_input import read_input
from inputs.input_analizer import InputAnalizer

# HEIGHT, WIDTH = 100, 200
# MAP_TYPE = "VORONOI"  # HEX|VORONOI

HEIGHT, WIDTH = 200, 300
MAP_TYPE = "HEX"  # HEX|VORONOI

size = 100


input = read_input("input_map_check.json")
analizer = InputAnalizer()
all_schemas = analizer.verify_input_format(input)

world_name = input["map_config"]["world_name"]
draw_schema(world_name, all_schemas[world_name]["continent_names"], all_schemas[world_name]["continent_schema"])

exit(0)

world_map = Map(WIDTH, HEIGHT, size, MAP_TYPE)



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
continent2 = Continent((150, 150), "Europe", world_map)
continent3 = Continent((100, 100), "America", world_map)
for i in range(50):
    continent1.increase_territory(world_map, 10)
    continent2.increase_territory(world_map, 10)
    continent3.increase_territory(world_map, 5)

draw_map(world_map, "before.png")

continent1.fill_holes(world_map)

terrains = read_terrains()

terrain1 = Terrain((45, 54), "A", "Plain", world_map, continent1, terrains)
terrain2 = Terrain((50, 45), "B", "Mountain", world_map, continent1, terrains)
terrain3 = Terrain((40, 45), "C", "Hill", world_map, continent1, terrains)
terrain4 = Terrain((110, 55), "D", "Mountain", world_map, continent2, terrains)
terrain5 = Terrain((105, 45), "E", "Plain", world_map, continent2, terrains)
terrain6 = Terrain((95, 45), "F", "Mountain", world_map, continent3, terrains)
terrain7 = Terrain((100, 51), "G", "Hill", world_map, continent3, terrains)

for i in range(50):
    terrain1.increase_territory(world_map, 10)
    terrain2.increase_territory(world_map, 10)
    terrain3.increase_territory(world_map, 10)
    terrain4.increase_territory(world_map, 10)
    terrain5.increase_territory(world_map, 10)
    terrain6.increase_territory(world_map, 10)
    terrain7.increase_territory(world_map, 10)

terrain1.set_height(world_map)
terrain2.set_height(world_map)
terrain3.set_height(world_map)
terrain4.set_height(world_map)
terrain5.set_height(world_map)
terrain6.set_height(world_map)
terrain7.set_height(world_map)

for i in range(10):
    river = River(world_map, continent1)
    world_map.rivers.append(river)

for i in range(10):
    river = River(world_map, continent2)
    world_map.rivers.append(river)


world_map.rivers_finalize()


races = read_races()

cities = []
for i in range(25):
    city = City("city" + str(i), continent1, world_map, races, "Human")
    cities.append(city)
world_map.cities += cities

cities = []
for i in range(25):
    city = City("city" + str(i), continent2, world_map, races, "Human")
    cities.append(city)
world_map.cities += cities

draw_map(world_map, "after.png")

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
world_map.create_roads(world_map, continent2, terrains, bioms)
world_map.create_roads(world_map, continent3, terrains, bioms)

draw_map(world_map, "bioms.png")