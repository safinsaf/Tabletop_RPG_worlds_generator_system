class Cell:

    center = (0, 0)
    borders = [(0,0), (0,0), (0,0), (0,0)]
    color = (0,0,0,0)
    level_0 = "Sea"     #"Continent"

    def __init__(self, center, borders):
        self.center = center
        self.borders = borders

