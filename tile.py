class Tile:
    def __init__(self, color, number, is_joker=False):
        self.color = color
        self.number = number
        self.is_joker = is_joker

    def __repr__(self):
        if self.is_joker:
            return "Joker"
        return f"{self.color}{self.number}"
