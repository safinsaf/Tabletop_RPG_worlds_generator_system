
import logging

from plugins.__read_bioms__ import read_bioms

class InputFormatVerifier():

    continent_names = []
    terrain_names = []
    biom_names = []

    bioms_data = []

    relative_locations = [
        "west",
        "east",
        "north",
        "south",
        "north-west",
        "north-east",
        "south-west",
        "south-east", 
    ]

    relative_location_inverts = {
        "west": "east",
        "east": "west",
        "north": "south",
        "south": "north",
        # "north-west": "south-east",
        # "north-east": "south-west",
        # "south-west": "north-east",
        # "south-east": "north-west",
    }

    relative_locations_divide = {
        "west": ["west"],
        "east": ["east"],
        "north": ["north"],
        "south": ["south"],
        "north-west": ["north", "west"],
        "north-east": ["north", "east"],
        "south-west": ["south", "west"],
        "south-east": ["south", "east"],
    }

    def verify_input(self, input):
        map_config = input["map_config"]
        continents = input["continents"]
        terrains = input["terrains"]
        biomes = input["biomes"]
        
        river_clusters = input["river_clusters"]
        city_clusters = input["city_clusters"]
        
        continents_relative_location = input["continents_relative_location"]
        terrains_relative_location = input["terrains_relative_location"]
        biomes_relative_location = input["biomes_relative_location"]

        self.verify_map_config(map_config)

        self.verify_continents(continents)
        self.verify_continents_unique(continents)
        self.set_continent_names(continents)
        
        self.verify_terrains(terrains)
        self.verify_terrains_unique(terrains)
        self.verify_terrains_belong_to_existing_continents(terrains)
        self.set_terrain_names(terrains)

        self.read_biomes()
        self.verify_bioms(biomes)
        self.verify_biomes_unique(biomes)
        self.verify_biomes_belong_to_existing_continents(biomes)
        self.set_biom_names(biomes)

        self.verify_river_clusters(river_clusters)
        self.verify_river_clusters_belong_to_existing_continents(river_clusters)
        self.verify_continent_in_river_clusters_unique(river_clusters)

        self.verify_city_clusters(city_clusters)
        self.verify_city_clusters_belong_to_existing_continents(city_clusters)
        self.verify_continent_in_city_clusters_unique(city_clusters)

        self.verify_continents_relative_location(continents_relative_location)
        self.verify_continents_in_continents_relative_location_exist(continents_relative_location)

        self.verify_terrains_relative_location(terrains_relative_location)
        self.verify_terrains_in_terrains_relative_location_exist(terrains_relative_location)

        self.verify_biomes_relative_location(biomes_relative_location)
        self.verify_biomes_in_biomes_relative_location_exist(biomes_relative_location)
        

    def verify_map_config(self, map_config):

        assert "height" in map_config, "map_config must contain parameter height" 
        assert type(map_config["height"]) == int, "Type of height in map_config must be int"
        assert int(map_config["height"]) > 0, "map height should be greater than 0" 
        
        assert "width" in map_config, "map_config must contain int parameter width" 
        assert type(map_config["width"]) == int, "type of width in map_config must be int"
        assert int(map_config["width"]) > 0, "map width should be greater than 0" 
        
        assert "size" in map_config, "map_config must contain int parameter size"
        assert type(map_config["size"]) == int, "type of size in map_config must be int" 
        assert int(map_config["size"]) > 0, "map size should be greater than 0" 
        
        assert "type" in map_config, "map_config must contain parameter type"
        assert type(map_config["type"]) == str, "type of type in map_config must be string" 
        assert map_config["type"] == "HEX" or map_config["type"] == "VORONOI", "type of map must be HEX or VORONOI"


    def verify_continents(self, continents):
        
        for continent in continents:
            assert "name" in continent, "all continents must have parameter name"
            assert type(continent["name"]), "type of continent name must be string"
            assert continent["name"] != "", "value of continent name must be nonempty"

    def verify_continents_unique(self, continents):
        continent_names = []
        for continent in continents:
            continent_names.append(continent["name"])
        continent_names_as_set = set(continent_names)
        
        assert len(continent_names_as_set) == len(continent_names), "continent names must be unique"


    def set_continent_names(self, continents):
        for continent in continents:
            self.continent_names.append(continent["name"])


    def verify_terrains(self, terrains):
        for terrain in terrains:
            assert "name" in terrain, "all terrains must have parameter name"
            assert type(terrain["name"]) == str, "type of terrain name must be string"
            assert terrain["name"] != "", "value of terrain name must be nonempty"

            assert "type" in terrain, "all terrains must have parameter type"
            assert type(terrain["type"]) == str, "type of terrain type must be string"
            assert terrain["type"] == "mountain" or terrain["type"] == "plain" or terrain["type"] == "hill", \
                "all terrain types must be hill, plain or mountain"

            assert "continent" in terrain, "all terrains must have parameter continent"
            assert type(terrain["continent"]) == str, "type of continent in terrain must be string"
            assert terrain["continent"] != "", "value of continent in terrain must be nonempty"

    
    def verify_terrains_unique(self, terrains):
        terrain_names = []
        for terrain in terrains:
            terrain_names.append(terrain["name"])
        terrain_names_as_set = set(terrain_names)

        assert len(terrain_names_as_set) == len(terrain_names), "terrain names must be unique"


    def verify_terrains_belong_to_existing_continents(self, terrains):
        for terrain in terrains:
            assert terrain["continent"] in self.continent_names, "continent in terrains must exist"


    def set_terrain_names(self, terrains):
        for terrain in terrains:
            self.terrain_names.append(terrain["name"])


    def read_biomes(self):
        self.biomes_data = read_bioms()
        

    def verify_bioms(self, biomes):
        for biom in biomes:
            assert "name" in biom, "all biomes must have parameter name"
            assert type(biom["name"]) == str, "type of biom name must be string"
            assert biom["name"] != "", "value of biom name must be nonempty"

            assert "type" in biom, "all biomes must have parameter type"
            assert type(biom["type"]) == str, "type of biom type must be string"
            assert biom["type"] in self.biomes_data, "value of biom type must be in {self.biomes_data}"

            assert "continent" in biom, "all biomes must have parameter continent"
            assert type(biom["continent"]) == str, "type of continent in biom must be string"
            assert biom["continent"] != "", "value of continent in biom must be nonempty"


    def verify_biomes_unique(self, biomes):
        biom_names = []
        for biom in biomes:
            biom_names.append(biom["name"])
        biom_names_as_set = set(biom_names)

        assert len(biom_names_as_set) == len(biom_names), "biom names must be unique"



    def verify_biomes_belong_to_existing_continents(self, biomes):
        for biom in biomes:
            assert biom["continent"] in self.continent_names, "continents in biomes must exist"


    def set_biom_names(self, biomes):
        for biom in biomes:
            self.biom_names.append(biom["name"])


    def verify_river_clusters(self, river_clusters):
        for river_cluster in river_clusters:
            assert "count" in river_cluster, "all river_clusters must have parameter count"
            assert type(river_cluster["count"]) == int, "type of count in river_cluster must be int"
            assert river_cluster["count"] >= 0, "value of count in river_cluster must be >= 0"

            assert "continent" in river_cluster, "all river_clusters must have parameter continent"
            assert type(river_cluster["continent"]) == str, "type of continent in river_cluster must be string"
            assert river_cluster["continent"] != "", "value of continent in river_cluster must be nonempty"


    def verify_river_clusters_belong_to_existing_continents(self, river_clusters):
        for river_cluster in river_clusters:
            assert river_cluster["continent"] in self.continent_names, "continents in river_clusters must exist"
        

    def verify_continent_in_river_clusters_unique(self, river_clusters):
        continent_names = []
        for river_cluster in river_clusters:
            continent_names.append(river_cluster["continent"])
        continent_names_as_set = set(continent_names)

        assert len(continent_names_as_set) == len(continent_names), "continents in river_clusters must be unique"


    def verify_city_clusters(self, city_clusters):
        for city_cluster in city_clusters:
            assert "count" in city_cluster, "all city_clusters must have parameter count"
            assert type(city_cluster["count"]) == int, "type of count in city_cluster must be int"
            assert city_cluster["count"] >= 0, "value of count in city_cluster must be >= 0"

            assert "continent" in city_cluster, "all city_clusters must have parameter continent"
            assert type(city_cluster["continent"]) == str, "type of continent in city_cluster must be string"
            assert city_cluster["continent"] != "", "value of continent in city_cluster must be nonempty"


    def verify_city_clusters_belong_to_existing_continents(self, city_clusters):
        for city_cluster in city_clusters:
            assert city_cluster["continent"] in self.continent_names, "continents in city_clusters must exist"
        

    def verify_continent_in_city_clusters_unique(self, city_clusters):
        continent_names = []
        for city_cluster in city_clusters:
            continent_names.append(city_cluster["continent"])
        continent_names_as_set = set(continent_names)

        assert len(continent_names_as_set) == len(continent_names), "continents in city_clusters must be unique"



    def verify_continents_relative_location(self, continents_relative_location):

        for relation in continents_relative_location:
            assert "first" in relation, "each continent relation must contain parameter first"
            assert type(relation["first"]) == str, "type of first parameter in continent relation must be string"
            assert relation["first"] != "", "value of first parameter in continent relation must be nonempty"

            assert "second" in relation, "each continent relation must contain parameter second"
            assert type(relation["second"]) == str, "type of second parameter in continent relation must be string"
            assert relation["second"] != "", "value of second parameter in continent relation must be nonempty"

            assert "location" in relation, "each continent relation must contain parameter location"
            assert type(relation["location"]) == str, "type of parameter location in relation must be string"
            location = relation["location"].split()
            assert len(location) == 3 and location[0] == "on" and location[2] == "of", \
                "location parameter must have format 'in north of' "
            assert location[1] in self.relative_locations, \
                f"value of relation must be one of 'on' {self.relative_locations} 'of', but not 'on' " + location[1] + " 'of'"

    def verify_continents_in_continents_relative_location_exist(self, continents_relative_location):
        for relation in continents_relative_location:
            assert relation["first"] in self.continent_names, \
                f"continent " + relation["first"] + f" does not exist. Existing continents are {self.continent_names}"

            assert relation["second"] in self.continent_names, \
                f"continent " + relation["second"] + f" does not exist. Existing continents are {self.continent_names}"

            assert relation["first"] != relation["second"], \
                "continent " + relation["first"] + " can not relate to itself"

    def verify_terrains_relative_location(self, terrains_relative_location):

        for relation in terrains_relative_location:
            assert "first" in relation, "each terrain relation must contain parameter first"
            assert type(relation["first"]) == str, "type of first parameter in terrain relation must be string"
            assert relation["first"] != "", "value of first parameter in terrain relation must be nonempty"

            assert "second" in relation, "each terrain relation must contain parameter second"
            assert type(relation["second"]) == str, "type of second parameter in terrain relation must be string"
            assert relation["second"] != "", "value of second parameter in terrain relation must be nonempty"

            assert "location" in relation, "each terrain relation must contain parameter location"
            assert type(relation["location"]) == str, "type of parameter location in relation must be string"
            location = relation["location"].split()
            assert len(location) == 3 and location[0] == "on" and location[2] == "of", \
                "location parameter must have format 'in north of' "
            assert location[1] in self.relative_locations, \
                f"value of relation must be one of 'on' {self.relative_locations} 'of', but not 'on' " + location[1] + " 'of'"

            assert "continent" in relation, "each terrain relation must contain parameter continent"
            assert type(relation["continent"]) == str, "type of continent parameter in terrain must be string"
            assert relation["continent"] != "", "value of continent parameter in terrain must be nonempty"
            assert relation["continent"] in self.continent_names, \
                f"value of continent in terrain relations must be in {self.continent_names}, but not " + relation["continent"]

    def verify_terrains_in_terrains_relative_location_exist(self, terrains_relative_location):
        for relation in terrains_relative_location:
            assert relation["first"] in self.terrain_names, \
                f"terrain " + relation["first"] + f" does not exist. Existing terrains are {self.terrain_names}"

            assert relation["second"] in self.terrain_names, \
                f"terrain " + relation["second"] + f" does not exist. Existing terrains are {self.terrain_names}"

            assert relation["first"] != relation["second"], \
                "terrain " + relation["first"] + " can not relate to itself"

    def verify_biomes_relative_location(self, biomes_relative_location):
        for relation in biomes_relative_location:
            assert "first" in relation, "each biom relation must contain parameter first"
            assert type(relation["first"]) == str, "type of first parameter in biom relation must be string"
            assert relation["first"] != "", "value of first parameter in biom relation must be nonempty"

            assert "second" in relation, "each biom relation must contain parameter second"
            assert type(relation["second"]) == str, "type of second parameter in biom relation must be string"
            assert relation["second"] != "", "value of second parameter in biom relation must be nonempty"

            assert "location" in relation, "each biom relation must contain parameter location"
            assert type(relation["location"]) == str, "type of parameter location in relation must be string"
            location = relation["location"].split()
            assert len(location) == 3 and location[0] == "on" and location[2] == "of", \
                "location parameter must have format 'in north of' "
            assert location[1] in self.relative_locations, \
                f"value of relation must be one of 'on' {self.relative_locations} 'of', but not 'on' " + location[1] + " 'of'"

            assert "continent" in relation, "each biom relation must contain parameter continent"
            assert type(relation["continent"]) == str, "type of continent parameter in biom must be string"
            assert relation["continent"] != "", "value of continent parameter in biom must be nonempty"


    def verify_biomes_in_biomes_relative_location_exist(self, biomes_relative_location):
        for relation in biomes_relative_location:
            assert relation["first"] in self.biom_names, \
                f"biom " + relation["first"] + f" does not exist. Existing biomes are {self.biom_names}"

            assert relation["second"] in self.biom_names, \
                f"biom " + relation["second"] + f" does not exist. Existing biomes are {self.biom_names}"

            assert relation["first"] != relation["second"], \
                "biom " + relation["first"] + " can not relate to itself"