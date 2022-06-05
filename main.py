from app.city import City
from app.continent import Continent
from app.map import Map
from app.river import River
from app.terrain import Terrain
from app.biom import Biom
from app.input_analizer import InputAnalizer
from app.choose_ponts import CoordsFinder
from app.draw import Drawer

from app.read_terrains import read_terrains
from app.read_biomes import read_biomes
from app.read_races import read_races
from app.read_input import read_input

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


drawer.draw_map(world_map, "Continents")

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


biomes_info = read_biomes()

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