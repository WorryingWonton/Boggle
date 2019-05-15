import unittest
from itertools import permutations
from boggle import Boggle, Player
from math import sqrt

#Unit Test specific version of Boggle which overrides check_if_valid_english(), but is otherwise unaltered.
class UTBoggle(Boggle):

    def find_word(self, word, trace_word):
        for row in self.board.spaces:
            for space in row:
                if self.trace_path(trace_word, space, set()):
                    return True
        return False


class TestBoggle(unittest.TestCase):

    def test_find_word_2x2(self):
        game_instance = UTBoggle(grid_size=2, max_rounds=1)
        test_board = self.generate_test_board('NSSN')
        game_instance = self.map_tls_to_board(game_instance, test_board)
        my_string = 'nssn'
        words = []
        self.assertEqual(False, game_instance.find_word(None, 'sss'))
        self.assertEqual(False, game_instance.find_word(None, 'ssnnn'))
        self.assertEqual(False, game_instance.find_word(None, 'nnn'))
        for r in range(1, 5):
            words += [''.join(x) for x in list(permutations(my_string, r=r))]
        for word in words:
            self.assertEqual(True, game_instance.find_word(trace_word=word, word=None))

    def test_find_word_3x3(self):
        pass

    def test_find_word_4x4(self):
        game_instance = UTBoggle(grid_size=4, max_rounds=1)
        test_board = self.generate_test_board('MPOWXYZTFABCNLSH')
        game_instance = self.map_tls_to_board(game_instance, test_board)
        word = 'mpow'
        self.assertEqual(True, game_instance.find_word(None, word))
        tb_2 = self.generate_test_board('BZ@IXRIFJCEMPTRA')
        gi_2 = UTBoggle(grid_size=4, max_rounds=1)
        gi_2 = self.map_tls_to_board(gi_2, tb_2)
        self.assertEqual(True, gi_2.find_word(None, '@iz'))
        self.assertEqual(True, gi_2.find_word(None, 'art'))
        self.assertEqual(True, gi_2.find_word(None, 'ptjc'))
        self.assertEqual(True, gi_2.find_word(None, 'bz@ii'))

    def test_boggle_score_round(self):
        game_instance = UTBoggle(max_rounds=3, grid_size=5)
        game_instance.players = [Player(name='ll'), Player(name='kk')]
        game_instance.players[0].words = {0: {'hello': 2, 'hiii': 1}, 1: {'hey': 1, 'there': 2}, 2: {'soo': 1, 'what': 1}}
        game_instance.players[1].words = {0: {'hello': 2, 'xxxxxx': 3}, 1: {'hey': 1, 'tharr': 2}, 2: {'soo': 1, 'nutttt': 3}}
        game_instance.score_round()
        self.assertEqual(1, game_instance.players[0].score)
        self.assertEqual(3, game_instance.players[1].score)

    def map_tls_to_board(self, game_instance, test_board_tls):
        for r_idx, row in enumerate(game_instance.board.spaces):
            for s_idx, space in enumerate(row):
                space.cube.top_letter_lc = test_board_tls[r_idx][s_idx].lower()
                space.cube.top_letter = test_board_tls[r_idx][s_idx]
        return game_instance

    def generate_test_board(self, string):
        #string must always be a perfect square in length
        root_length = int(sqrt(len(string)))
        if sqrt(len(string)) % 1 != 0:
            raise Exception(f'len(string) must be a perfect square, {len(string)} is not a perfect square.')
        else:
            string_array = []
            for i in range(root_length):
                string_array.append(list(string[0:root_length]))
                string = string[root_length:]
            return string_array

if __name__ == '__main__':
    unittest.main()