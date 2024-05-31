import random
from tile import Tile

class Deck:
    colors = ['R', 'B', 'G', 'Y']  # Red, Blue, Green, Yellow

    def __init__(self):
        self.tiles = [Tile(color, number) for color in self.colors for number in range(1, 14) for _ in range(2)]
        self.tiles.append(Tile(None, None, is_joker=True))  # Add first joker
        self.tiles.append(Tile(None, None, is_joker=True))  # Add second joker
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.tiles)

    def draw(self):
        return self.tiles.pop() if self.tiles else None

