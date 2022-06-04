from city import City
from continent import Continent
from map import Map
from river import River
from terrain import Terrain
from biom import Biom
from terrains.__read_terrains__ import read_terrains
from plugins.__read_bioms__ import read_bioms
from races.__read_races__ import read_races
from draw import Drawer

from inputs.read_input import read_input
from inputs.input_analizer import InputAnalizer
from inputs.choose_ponts import CoordsFinder

# HEIGHT, WIDTH = 100, 200
# MAP_TYPE = "VORONOI"  # HEX|VORONOI

#HEIGHT, WIDTH = 200, 300
#MAP_TYPE = "HEX"  # HEX|VORONOI
#size = 100


input = read_input("input.json")
analizer = InputAnalizer()
all_schemas = analizer.verify_input_format(input)

print(all_schemas)

world_name = input["map_config"]["world_name"]
height = input["map_config"]["height"]
width = input["map_config"]["width"]
map_type = input["map_config"]["type"]
size = input["map_config"]["size"]

drawer = Drawer()
drawer.draw_schema(world_name, all_schemas[world_name]["continent_names"], all_schemas[world_name]["continent_schema"])
for continent_name in all_schemas[world_name]["continent_names"]:
    drawer.draw_schema(continent_name + "_terrains", all_schemas[continent_name]["terrain_names"], all_schemas[continent_name]["terrain_schema"])
    drawer.draw_schema(continent_name + "_bioms", all_schemas[continent_name]["biom_names"], all_schemas[continent_name]["biom_schema"])


world_map = Map(width, height, size, map_type)

drawer.draw_map(world_map, "ocean")

image_size = world_map.image_size()
coords_finder = CoordsFinder()
#print([ coords for coords in world_map.all_cell_indexes() ])
continent_coords = coords_finder.find_coords(
    world_map,
    world_map,
    all_schemas[world_name]["continent_schema"],
    all_schemas[world_name]["continent_names"]
    )

continents = []
for i in range(len(all_schemas[world_name]["continent_names"])):
    continent_name = all_schemas[world_name]["continent_names"][i]
    continent = Continent(continent_coords[i],continent_name, world_map)
    continents.append(continent)

continent_size = int(height * width / 4 // len(continents))
for i in range(continent_size // 10):
    for j in range(len(continents)):
        continent = continents[j]
        continent.increase_territory(world_map, 10)

for continent in continents:
    continent.fill_holes(world_map)


drawer.draw_map(world_map, "Bare_continents")

terrains_info = read_terrains()

for continent in continents:
    terrain_coords = coords_finder.find_coords(
        continent,
        world_map,
        all_schemas[continent.name]["terrain_schema"],
        all_schemas[continent.name]["terrain_names"]
        )

    terrains = []
    for i in range(len(all_schemas[continent.name]["terrain_names"])):
        terrain_name = all_schemas[continent.name]["terrain_names"][i]
        terrain_type = all_schemas[continent.name]["terrain_types"][terrain_name]
        terrain = Terrain(terrain_coords[i], terrain_name, terrain_type, world_map, continent, terrains_info)
        terrains.append(terrain)

    continent_size = len(continent.coords_arr) 
    for i in range(continent_size // 10 + 50):
        for j in range(len(terrains)):
            terrain = terrains[j]
            terrain.increase_territory(world_map, 10)
    
    for i in range(len(terrains)):
        terrain = terrains[i]
        terrain.set_height(world_map)

drawer.draw_map(world_map, "Terrains")


biomes_info = read_bioms()

for continent in continents:
    biom_coords = coords_finder.find_coords(
        continent,
        world_map,
        all_schemas[continent.name]["biom_schema"],
        all_schemas[continent.name]["biom_names"]
        )

    biomes = []
    for i in range(len(all_schemas[continent.name]["biom_names"])):
        biom_name = all_schemas[continent.name]["biom_names"][i]
        biom_type = all_schemas[continent.name]["biom_types"][biom_name]
        coords = biom_coords[i]
        biom = Biom(biom_coords[i], biom_name, biom_type, biomes_info)
        
        if biom.is_restricted(coords[0], coords[1], world_map):
            points = []
            for cont_coord in continent.coords_arr:
                if not biom.is_restricted(cont_coord[0], cont_coord[1], world_map):
                    points.append(cont_coord)
            
            if len(points) == 0:
                print("All terrains are restricted in ", continent.name, " for ", biom_name)
                exit(0)

            new_biom_coord = coords_finder.find_closest_point(coords, points)[1]

            biom = Biom(new_biom_coord, biom_name, biom_type, biomes_info)    
        biomes.append(biom)

    continent_size = len(continent.coords_arr)
    for i in range(continent_size // 10 + 50):
        for j in range(len(biomes)):
            biom = biomes[j]
            biom.increase_territory(world_map, 10)

drawer.draw_map(world_map, "Biomes")


for continent in continents:
    
    rivers_count = all_schemas[continent.name]["rivers_count"]

    for i in range(rivers_count):
        river = River(world_map, continent)
        world_map.rivers.append(river)

world_map.rivers_finalize()

drawer.draw_map(world_map, "Rivers")

races_info = read_races()

for continent in continents:
    
    cities_count = all_schemas[continent.name]["cities_count"]

    cities = []
    for i in range(cities_count):
        city = City("city" + str(i), continent, world_map, races_info, "human")
        cities.append(city)
    world_map.cities += cities
    

drawer.draw_map(world_map, "Cities")

for continent in continents:
    world_map.create_roads(world_map, continent, terrains_info, biomes_info)

drawer.draw_map(world_map, "Roads")



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

# continent1 = Continent((40, 50), "Asia", world_map)
# continent2 = Continent((150, 150), "Europe", world_map)
# continent3 = Continent((100, 100), "America", world_map)
# for i in range(50):
#     continent1.increase_territory(world_map, 10)
#     continent2.increase_territory(world_map, 10)
#     continent3.increase_territory(world_map, 5)

# draw_map(world_map, "before")

# continent1.fill_holes(world_map)

# terrains = read_terrains()

# terrain1 = Terrain((45, 54), "A", "Plain", world_map, continent1, terrains)
# terrain2 = Terrain((50, 45), "B", "Mountain", world_map, continent1, terrains)
# terrain3 = Terrain((40, 45), "C", "Hill", world_map, continent1, terrains)
# terrain4 = Terrain((110, 55), "D", "Mountain", world_map, continent2, terrains)
# terrain5 = Terrain((105, 45), "E", "Plain", world_map, continent2, terrains)
# terrain6 = Terrain((95, 45), "F", "Mountain", world_map, continent3, terrains)
# terrain7 = Terrain((100, 51), "G", "Hill", world_map, continent3, terrains)

# for i in range(50):
#     terrain1.increase_territory(world_map, 10)
#     terrain2.increase_territory(world_map, 10)
#     terrain3.increase_territory(world_map, 10)
#     terrain4.increase_territory(world_map, 10)
#     terrain5.increase_territory(world_map, 10)
#     terrain6.increase_territory(world_map, 10)
#     terrain7.increase_territory(world_map, 10)

# terrain1.set_height(world_map)
# terrain2.set_height(world_map)
# terrain3.set_height(world_map)
# terrain4.set_height(world_map)
# terrain5.set_height(world_map)
# terrain6.set_height(world_map)
# terrain7.set_height(world_map)

# for i in range(10):
#     river = River(world_map, continent1)
#     world_map.rivers.append(river)

# for i in range(10):
#     river = River(world_map, continent2)
#     world_map.rivers.append(river)


# world_map.rivers_finalize()


# races = read_races()

# cities = []
# for i in range(25):
#     city = City("city" + str(i), continent1, world_map, races, "Human")
#     cities.append(city)
# world_map.cities += cities

# cities = []
# for i in range(25):
#     city = City("city" + str(i), continent2, world_map, races, "Human")
#     cities.append(city)
# world_map.cities += cities

# draw_map(world_map, "after")

# bioms = read_bioms()

# biom1 = Biom((45, 45), "Forest A", "Forest", bioms)
# biom2 = Biom((50, 60), "Swamp B", "Swamp", bioms)
# biom3 = Biom((55, 55), "Desert C", "Desert", bioms)
# biom4 = Biom((60, 35), "Tundra A", "Tundra", bioms)

# print(dir(world_map.cells[45][45]))

# for i in range(100):
#     biom1.increase_territory(world_map, 10)
#     biom2.increase_territory(world_map, 10)
#     biom3.increase_territory(world_map, 5)
#     biom4.increase_territory(world_map, 10)


# world_map.create_roads(world_map, continent1, terrains, bioms)
# world_map.create_roads(world_map, continent2, terrains, bioms)
# world_map.create_roads(world_map, continent3, terrains, bioms)

# draw_map(world_map, "bioms")