class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_tile(self, deck):
        tile = deck.draw()
        if tile:
            self.hand.append(tile)

    def play_tiles(self, tiles):
        for tile in tiles:
            self.hand.remove(tile)

    def __repr__(self):
        return f"{self.name}: {self.hand}"
