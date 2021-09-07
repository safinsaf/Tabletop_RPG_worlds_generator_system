import codecs
import os
from fnmatch import fnmatch
from json import load

root = "./plugins"
pattern = "*.json"


def read_bioms():
    plugins = {}

    for path, _, files in os.walk(root):
        for name in files:
            if not fnmatch(name, pattern):
                continue
            plugin_name = name[:-5]
            # fileObj = codecs.open(path + "/" + name, encoding="utf-8", mode="rb", errors="ignore")
            # file = fileObj.read()
            with open(
                path + "/" + name, encoding="UTF-8", errors="ignore"
            ) as json_file:
                file = load(json_file)
            plugins[plugin_name] = file

    return plugins