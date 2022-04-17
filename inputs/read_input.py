import os
from fnmatch import fnmatch
from json import load

ROOT = "./inputs"
PATTERN = "*.json"


def read_input(filename):
    input = {}

    for path, _, files in os.walk(ROOT):
        if filename in files:
            input_name = filename[:-5]
            with open(
                path + "/" + filename, encoding="UTF-8", errors="ignore"
            ) as json_file:
                file = load(json_file)
            input = file

    return input
