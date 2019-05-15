import random
import string
from boggle_cl_interface import BoggleInterface

class Boggle:

    def __init__(self, grid_size, max_rounds, interface=None,  scoring_model=None, max_players=None):
        self.board = Board(grid_size)
        self.players = []
        self.max_rounds = max_rounds
        self.current_round = 0
        self.interface = interface
        if not self.interface:
            self.interface = BoggleInterface(game_instance=self)
        self.scoring_model = scoring_model
        if not self.scoring_model:
            self.scoring_model = [(0, 0), (3, 1), (4, 1), (5, 2), (6, 3), (7, 5), (8, 11)]
        self.max_players = max_players
        if not max_players:
            self.max_players = 2

    def add_players(self):
        names = self.interface.get_player_names()
        for name in names:
            self.players.append(Player(name=name))

    def run_game(self):
        for player in self.players:
            player.build_score_dict(self.max_rounds)
        while self.current_round < self.max_rounds:
            self.run_round()
            self.current_round += 1
            self.board.shuffle_cubes()
            self.board.shake_cubes()
        return max(self.players, key=lambda x: x.score)

    def run_round(self):
        for player in self.players:
            self.run_turn(player)
        self.score_round()

    def run_turn(self, active_player):
        self.interface.display_board()
        self.interface.display_scores()
        words = self.interface.get_words(active_player)
        trace_words = self.handle_qu(words)
        for idx, word in enumerate(words):
            if self.find_word(trace_words[idx]):
                active_player.words[self.current_round][word] = self.score_word(word)

    def handle_qu(self, words):
        return ['@'.join(word.split('qu')) for word in words]

    def find_word(self, word):
        if not self.check_if_valid_english(word=word):
            return False
        for row in self.board.spaces:
            for space in row:
                if self.trace_path(word, space, set()):
                    return True
        return False

    def trace_path(self, word, space, consumed_spaces):
        if len(word) == 1 and word == space.cube.top_letter_lc:
            return True
        elif word[0] != space.cube.top_letter_lc:
            return False
        else:
            for neighbor in filter(lambda x: x not in consumed_spaces, space.adjacents):
                if self.trace_path(word[1:], neighbor, consumed_spaces | {space}):
                    return True

    def check_if_valid_english(self, word):
        if not word:
            return False
        return True

    def score_word(self, word):
        for idx, tup in enumerate(self.scoring_model):
            if len(word) < tup[0]:
                return self.scoring_model[idx - 1][1]
        return self.scoring_model[-1][1]

    def score_round(self):
        for player in self.players:
            for word in player.words[self.current_round]:
                if word in sum([list(x.words[self.current_round].keys()) for x in self.players if x is not player], []):
                    player.words[self.current_round][word] = 0
            player.compute_score(self.current_round)


class Player:

    def __init__(self, name):
        self.name = name
        self.words = {}
        self.score = 0

    def build_score_dict(self, max_rounds):
        self.words = {x: {} for x in range(max_rounds)}

    def compute_score(self, current_round):
        self.score += sum(self.words[current_round].values())


class Board:

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.spaces = []
        self.cubes = []
        if not self.cubes:
            self.make_cubes()
        if not self.spaces:
            self.populate_spaces()

    def populate_spaces(self):
        # Run this method only once!
        count = 0
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                row.append(Space(x_coord=x, y_coord=y, cube=self.cubes[count]))
                count += 1
            self.spaces.append(row)
        self.generate_adjacents()

    def generate_adjacents(self):
        for row in self.spaces:
            for space in row:
                space.find_adjacents(board=self.spaces)

    def make_cubes(self):
        self.cubes = [x() for x in [Cube]*(self.grid_size ** 2)]

    def shuffle_cubes(self):
        self.cubes = random.sample(self.cubes, k=len(self.cubes))

    def shake_cubes(self):
        for x in self.cubes:
            x.roll_cube()


class Space:

    def __init__(self, x_coord, y_coord, cube):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.cube = cube
        if not self.cube.letters:
            self.cube.generate_letters()
        self.adjacents = []

    def find_adjacents(self, board):
        for y in [1, 0, -1]:
            if self.y_coord + y not in range(len(board)):
                continue
            for x in [1, 0, -1]:
                if self.x_coord + x not in range(len(board)):
                    continue
                self.adjacents.append(board[self.y_coord + y][self.x_coord + x])
        self.adjacents.remove(self)

    def __str__(self):
        return self.cube.top_letter_lc


class Cube:

    def __init__(self):
        self.letters = []
        if not self.letters:
            self.generate_letters()
        self.top_letter = self.letters[0]
        self.top_letter_lc = self.letters[0].lower()

    def generate_letters(self):
        self.letters = list(map(lambda x: x + 'u' if x == 'Q' else x, random.choices(string.ascii_uppercase, k=6)))

    def roll_cube(self):
        self.top_letter = self.letters[random.randrange(6)]
        self.top_letter_lc = self.top_letter.lower() if self.top_letter != 'Qu' else '@'


if __name__ == '__main__':
    game = Boggle(grid_size=4, max_rounds=3)
    game.add_players()
    game.run_game()