import os
from fnmatch import fnmatch
from json import load

ROOT = "./inputs/biomes"
PATTERN = "*.json"


def read_biomes():
    plugins = {}

    for path, _, files in os.walk(ROOT):
        for name in files:
            if not fnmatch(name, PATTERN):
                continue
            plugin_name = name[:-5]
            with open(
                path + "/" + name, encoding="UTF-8", errors="ignore"
            ) as json_file:
                file = load(json_file)
            plugins[plugin_name] = file

    return plugins
