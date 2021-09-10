import os
from fnmatch import fnmatch
from json import load

ROOT = "./terrains"
PATTERN = "*.json"


def read_terrains():
    terrains = {}

    for path, _, files in os.walk(ROOT):
        for name in files:
            if not fnmatch(name, PATTERN):
                continue
            terrain_name = name[:-5]
            with open(
                path + "/" + name, encoding="UTF-8", errors="ignore"
            ) as json_file:
                file = load(json_file)
            terrains[terrain_name] = file

    return terrains
