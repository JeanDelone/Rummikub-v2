from deck import Deck
from player import Player
from board import Board
from enum import Enum, auto
from tile import Tile

class Game:
    def __init__(self, player_names:list):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.board = Board()
        self.current_player_idx = 0

    def deal_tiles(self):
        for _ in range(14):
            for player in self.players:
                player.draw_tile(self.deck)

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def play_turn(self, player):
        initial_hand_size = len(player.hand)
        board_backup = self.board.tiles.copy()
        hand_backup = player.hand.copy()


        if not self.is_valid_board() or len(player.hand) >= initial_hand_size:
            print(f"{player.name}'s move is invalid. Reverting.")
            self.revert_turn(player, board_backup, hand_backup)
            return

        print(f"{player.name} played their turn successfully.")
        self.next_player()

    def revert_turn(self, player, board_backup, hand_backup):
        player.hand = hand_backup
        self.board.tiles = board_backup



    def is_game_over(self):
        return any(len(player.hand) == 0 for player in self.players)

    def play_game(self):
        self.deal_tiles()
        while not self.is_game_over():
            current_player = self.players[self.current_player_idx]
            print(f"{current_player.name}'s turn")
            self.next_player()
    

    """
    Board and tiles validations
    Runs are continuous numbers with the same color (R1, R2, R3)
    Groups are same numbers with different colors (R1, B1, G1)
    """
    def is_valid_board(self):
        for group in self.board.tiles:
            if not (self.is_valid_run(group) or self.is_valid_set(group)):
                return False
        return True
    

    @staticmethod
    def is_valid_run(tiles):
        if len(tiles) < 3:
            return False

        non_joker_tiles = [tile for tile in tiles if not tile.is_joker]
        joker_count = len(tiles) - len(non_joker_tiles)

        if not non_joker_tiles:
            return False

        non_joker_tiles.sort(key=lambda x: x.number)

        color = non_joker_tiles[0].color
        for tile in non_joker_tiles:
            if tile.color != color:
                return False

        gaps = 0
        for i in range(1, len(non_joker_tiles)):
            gap = non_joker_tiles[i].number - non_joker_tiles[i - 1].number - 1
            gaps += gap

        return gaps <= joker_count


    @staticmethod
    def is_valid_group(tiles):
        if len(tiles) != 3 and len(tiles) != 4:
            return False

        non_joker_tiles = [tile for tile in tiles if not tile.is_joker]
        joker_count = len(tiles) - len(non_joker_tiles)

        if not non_joker_tiles:
            return False

        numbers = [tile.number for tile in non_joker_tiles]
        colors = [tile.color for tile in non_joker_tiles]

        if len(set(numbers)) == 1:
            return len(set(colors)) == len(colors) + joker_count
        elif len(set(colors)) == 1:
            non_joker_tiles.sort(key=lambda x: x.number)
            for i in range(1, len(non_joker_tiles)):
                if non_joker_tiles[i].number != non_joker_tiles[i-1].number + 1:
                    return False
            return True
        return False

    

    """
    Player actions
    In rummikub there are 4 possible actions listed below
    """
    def draw_tile(self, player):
        player.draw_tile(self.deck)

    def play_new_set(self, player, tiles):
        if self.is_valid_set(tiles) or self.is_valid_run(tiles):
            self.board.play_set(tiles)
            player.play_tiles(tiles)
            return True
        return False
    
    def add_to_existing_set(self, player, tiles, set_index):
        existing_set = self.board.tiles[set_index]
        combined_set = existing_set + tiles
        if self.is_valid_set(combined_set) or self.is_valid_run(combined_set):
            self.board.tiles[set_index] = combined_set
            player.play_tiles(tiles)
            return True
        return False

    
    def rearrange_board(self, player, new_board_state):
        all_tiles = [tile for group in self.board.tiles for tile in group]
        all_tiles += player.hand
        
        for group in new_board_state:
            if not (self.is_valid_set(group) or self.is_valid_run(group)):
                return False
        
        self.board.tiles = new_board_state
        player.hand = [tile for tile in all_tiles if tile not in [tile for group in new_board_state for tile in group]]
        return True
    

# Quick testing
if __name__ == "__main__":
    game = Game(['Jan', 'Paweł', 'Pat', 'Mat'])
    print(game.is_valid_run([
        Tile(None, None, is_joker=True),
        Tile('R', 1),
        Tile('R', 2),
        Tile('R', 4),
        Tile('R', 5)]
    ))
    print(game.is_valid_run([
        Tile(None, None, is_joker=True),
        Tile('R', 1),
        Tile('R', 2),
        Tile('R', 4)]
    ))
    print(game.is_valid_run([
        Tile(None, None, is_joker=True),
        Tile('R', 1),
        Tile('R', 2),
        Tile('R', 5)]
    ))
    print(game.is_valid_run([
        Tile(None, None, is_joker=True),
        Tile('R', 1),
        Tile('R', 3),
        Tile('R', 5)]
    ))
    print(game.is_valid_run([
        Tile(None, None, is_joker=True),
        Tile('R', 1),
        Tile('R', 2)]
    ))



