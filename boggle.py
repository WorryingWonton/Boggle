import random
import string
from boggle_cl_interface import BoggleInterface

#Make the cubes a command line argument, using a \n delimited text file populated with 6 character strings
#See https://boardgames.stackexchange.com/questions/29264/boggle-what-is-the-dice-configuration-for-boggle-in-various-languages

class Boggle:

    def __init__(self, grid_size, max_rounds, interface=None,  scoring_model=None, max_players=None, dictionary=None):
        self.x_width = grid_size[0]
        self.y_width = grid_size[1]
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
        if not self.max_players:
            self.max_players = 2
        self.dictionary = dictionary
        if not self.dictionary:
            self.dictionary = 'boggle_words.txt'
        self.boggle_words = self.build_boggle_words()

    def build_boggle_words(self):
        words = open(self.dictionary, 'r').read().split('\n')
        return {x for x in words if self.scoring_model[1][0] <= len(x) <= 2 * self.x_width * self.y_width}

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
            if self.find_word(words[idx], trace_words[idx]):
                active_player.words[self.current_round][word] = self.score_word(word)

    def handle_qu(self, words):
        return ['@'.join(word.split('qu')) for word in words]

    def find_word(self, word, trace_word):
        if not self.check_if_valid_english(word=word):
            return False
        for row in self.board.spaces:
            for space in row:
                if self.trace_path(trace_word, space, set()):
                    return True
        return False

    def trace_path(self, word, space, consumed_spaces):
        if word[0] != space.cube.top_letter_lc:
            return False
        elif len(word) == 1:
            return True
        else:
            for neighbor in filter(lambda x: x not in consumed_spaces, space.adjacents):
                if self.trace_path(word[1:], neighbor, consumed_spaces | {space}):
                    return True

    def check_if_valid_english(self, word):
        if not word:
            return False
        else:
            return word in self.boggle_words

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
        self.x_width = grid_size[0]
        self.y_width = grid_size[1]
        self.spaces = []
        self.cubes = []
        if not self.cubes:
            self.make_cubes()
        if not self.spaces:
            self.populate_spaces()

    def populate_spaces(self):
        count = 0
        for y in range(self.y_width):
            row = []
            for x in range(self.x_width):
                row.append(Space(x_coord=x, y_coord=y, cube=self.cubes[count]))
                count += 1
            self.spaces.append(row)
        self.generate_adjacents()
        self.shake_cubes()

    def generate_adjacents(self):
        for row in self.spaces:
            for space in row:
                space.find_adjacents(board=self)

    def make_cubes(self):
        self.cubes = [x() for x in [Cube]*(self.x_width * self.y_width)]

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
            if self.y_coord + y not in range(board.y_width):
                continue
            for x in [1, 0, -1]:
                if self.x_coord + x not in range(board.x_width):
                    continue
                self.adjacents.append(board.spaces[self.y_coord + y][self.x_coord + x])
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
        weights = [6, 2, 2, 3, 11, 2, 2, 5, 6, 1, 1, 4, 2, 6, 7, 2, 1, 5, 6, 9, 3, 2, 3, 1, 3, 1]
        letters = random.choices(string.ascii_uppercase, k=6, weights=weights)
        self.letters = list(map(lambda x: x + 'u' if x == 'Q' else x, letters))

    def roll_cube(self):
        self.top_letter = self.letters[random.randrange(6)]
        self.top_letter_lc = self.top_letter.lower() if self.top_letter != 'Qu' else '@'


if __name__ == '__main__':
    game = Boggle(grid_size=(10, 10), max_rounds=3, max_players=1)
    game.add_players()
    game.run_game()

