import os
from json import load
from fnmatch import fnmatch

root = "./plugins"
pattern = "*.json"

def read_bioms():
    plugins = {}

    for path, subdirs, files in os.walk(root):
        for name in files:
            if not fnmatch(name, pattern):
                continue
            plugin_name = name[:-5]
            print(plugin_name)
            with open(path + "/" + name) as json_file:
                file = load(json_file)
            plugins[plugin_name] = file

    return plugins


#with open(filename) as json_file:
#    world = load(json_file)

#names = list(world.keys())
