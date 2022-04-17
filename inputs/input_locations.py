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

vertical_locations = [
    "north", "south"
]

gorizontal_locations = [
    "west", "east"
]

relative_location_inverts = {
    "west": "east",
    "east": "west",
    "north": "south",
    "south": "north",
}

relative_location_directional = {
    # direction, changed
    "west": ["west", False],
    "east": ["west", True],
    "north": ["south", False],
    "south": ["south", True],
}

relative_locations_divide = {
    "west": ["fixed", "west"],
    "east": ["fixed", "east"],
    "north": ["north", "fixed"],
    "south": ["south", "fixed"],
    "north-west": ["north", "west"],
    "north-east": ["north", "east"],
    "south-west": ["south", "west"],
    "south-east": ["south", "east"],
}

def vertical(direction):
    directions = relative_locations_divide[direction]
    return directions[0]

def gorizontal(direction):
    directions = relative_locations_divide[direction]
    return directions[1]

