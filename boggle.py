import random
from boggle_cl_interface import BoggleInterface


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
        return {x.lower() for x in words if self.scoring_model[1][0] <= len(x) <= self.x_width * self.y_width}

    def add_players(self):
        names = self.interface.get_player_names()
        for name in names:
            self.players.append(Player(name=name))
            self.players[-1].build_score_dict(max_rounds=self.max_rounds)

    def run_game(self):
        while self.current_round < self.max_rounds:
            self.run_round()
            self.current_round += 1
            self.board.shuffle_cubes()
            self.board.reassign_cubes()
            self.board.shake_cubes()
        self.interface.display_final_scores()
        return max(self.players, key=lambda x: x.score)

    def run_round(self):
        for player in self.players:
            self.run_turn(player)
        self.score_round()

    def run_turn(self, active_player):
        self.interface.display_board()
        self.interface.display_scores()
        words = self.interface.get_words(active_player)
        for word in words:
            if self.find_word(word):
                active_player.words[self.current_round][word] = self.score_word(word)

    def find_word(self, word):
        if not self.check_if_valid_english(word=word.lower()):
            return False
        for row in self.board.spaces:
            for space in row:
                if self.trace_path(word, space, set()):
                    return True
        return False

    def trace_path(self, word, space, consumed_spaces):
        if word[:len(space.cube.top_letter)] != space.cube.top_letter.upper():
            return False
        elif word == space.cube.top_letter.upper():
            return True
        else:
            for neighbor in filter(lambda x: x not in consumed_spaces, space.adjacents):
                if self.trace_path(word[len(space.cube.top_letter):], neighbor, consumed_spaces | {space}):
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
            op_words = sum([list(x.words[self.current_round].keys()) for x in self.players if x is not player], [])
            for word in player.words[self.current_round]:
                if word in op_words:
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

    def reassign_cubes(self):
        count = 0
        for row in self.spaces:
            for space in row:
                space.cube = self.cubes[count]
                count += 1

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


class Cube:

    def __init__(self):
        self.letters = []
        if not self.letters:
            self.generate_letters()
        self.top_letter = self.letters[0]

    def generate_letters(self):
        alphabet = {'A': 6, 'B': 2, 'C': 2, 'D': 3, 'E': 11, 'F': 2, 'G': 2, 'H': 5, 'I': 6, 'J': 1, 'K': 1, 'L': 4,
                    'M': 2, 'N': 6, 'O': 7, 'P': 2, 'Qu': 1, 'R': 5, 'S': 6, 'T': 9, 'U': 3, 'V': 2, 'W': 3, 'X': 1,
                    'Y': 3, 'Z': 1}
        self.letters = random.choices(list(alphabet.keys()), k=6, weights=list(alphabet.values()))

    def roll_cube(self):
        self.top_letter = self.letters[random.randrange(6)]


if __name__ == '__main__':
    game = Boggle(grid_size=(6, 6), max_rounds=2, max_players=2)
    game.add_players()
    game.run_game()
