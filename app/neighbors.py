relations = {
    "West": {"dx": -1, "dy": 0},
    "East": {"dx": 1, "dy": 0},
    "North": {"dx": 0, "dy": -1},
    "South": {"dx": 0, "dy": 1},
    "North-West": {"dx": -1, "dy": -1},
    "North-East": {"dx": 1, "dy": -1},
    "South-West": {"dx": -1, "dy": 1},
    "South-East": {"dx": 1, "dy": 1},
}

inverts = {
    "West": "East",
    "East": "West",
    "North": "South",
    "South": "North",
    "North-West": "South-East",
    "North-East": "South-West",
    "South-West": "North-East",
    "South-East": "North-West",
}
