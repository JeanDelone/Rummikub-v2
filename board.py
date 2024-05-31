class Board:
    def __init__(self):
        self.tiles = []

    def play_set(self, tile_set):
        self.tiles.append(tile_set)

    def __repr__(self):
        return f"Board: {self.tiles}"
