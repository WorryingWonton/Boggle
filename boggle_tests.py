import unittest
from boggle import Boggle, Board, BoggleInterface

"""
I want to fully validate my Boggle code.
I should test:
    -There is a way to verify is a word is correct per the rules of Boggle for a variety of board sizes, aspect ratios and alphabets
    -There is a mechanism for verifying that a word is valid english, and that said word is soored according to a pre-supplied model
    -That the same word chosen by two or more players will not count towards their score
    -That the game will run for a pre-set number of rounds
    -That the game supports one or more players
    -That the game will return the winning Player's name and score after the last round has expired.
"""


class TestableBoggle(Boggle):

    def find_word(self, word):
        """
        Modified to remove the check for valid English.
        :param word: Should be an all uppercase String
        :return: None
        """
        for row in self.board.spaces:
            for space in row:
                if self.trace_path(word, space, set()):
                    return True
        return False


class TestIfValidBoggle(unittest.TestCase):
    """
    Tests:
        -A single letter can be found on a board containing a single letter
        -A single letter can be found on a board containing multiple letters
        -Multi-Character top_letter values are valid
        -A word can be found consisting of letters in a horizontal line.
        -A word can be found consisting of letters in a vertical line.
        -A word can be found consisting of diagonal letters
        -(2+c)x(2+r) behavior (any board with non-edge/corner spaces)
            -2x2
            -3x3
            -4x4
            -6x6
            -3x4
            -4x3
            -1x5
            -5x1
            -10x2
            -2x10
        -A word can be found using a combination of horizontal, vertical, and diagonal moves
        -A word will not be counted if it uses the same letter on the board more than once
        -A word will not be counted if part of it is not on the board
    """
    def test_single_letter_board(self):
        test_string = 'A'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((1, 1), 1))
        self.assertEqual(True, boggle_instance.find_word(test_string))

    def test_find_single_letter_amongst_many(self):
        test_string = 'ABCDEFGHIJKLMNOP'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((4, 4), 1))
        for char in test_string:
            self.assertEqual(True, boggle_instance.find_word(char))

    def test_find_multi_character_top_letter(self):
        boggle_instance = TestableBoggle((5, 5), 1)
        boggle_instance.board.spaces[2][4].cube.top_letter = 'Quack'
        self.assertEqual(True, boggle_instance.find_word('QUACK'))

    def test_find_horizontal_letters(self):
        """Uses a 1 x 10 board
            -Checks left to right
            -Checks right to left
            -Verifies a word must be fully on the board
        """
        test_string = 'abcdefghij'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((10, 1), 1))
        self.assertEqual(True, boggle_instance.find_word(test_string.upper()))
        self.assertEqual(True, boggle_instance.find_word('DEF'))
        self.assertEqual(False, boggle_instance.find_word('CC'))
        self.assertEqual(False, boggle_instance.find_word('GHIJJ'))
        self.assertEqual(False, boggle_instance.find_word('AABC'))

    def test_find_vertical_letters(self):
        """Uses a 10x1 board
            -Checks bottom to top
            -Checks top to bottom
            -Verifies a word must be fully on the board"""
        test_string = 'abcdefghij'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((1, 10), 1))
        self.assertEqual(True, boggle_instance.find_word(test_string.upper()))
        self.assertEqual(True, boggle_instance.find_word('DEF'))
        self.assertEqual(False, boggle_instance.find_word('CC'))
        self.assertEqual(False, boggle_instance.find_word('GHIJJ'))
        self.assertEqual(False, boggle_instance.find_word('AABC'))

    def test_find_diagonal_letters(self):
        test_string = 'abcdefghijklmnopqrstuvwxy'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((5, 5), 1))
        # [['a', 'b', 'c', 'd', 'e'],
        #  ['f', 'g', 'h', 'i', 'j'],
        #  ['k', 'l', 'm', 'n', 'o'],
        #  ['p', 'q', 'r', 's', 't'],
        #  ['u', 'v', 'w', 'x', 'y']]
        self.assertEqual(True, boggle_instance.find_word('AGMSY'))
        self.assertEqual(True, boggle_instance.find_word('YSMGA'))
        self.assertEqual(True, boggle_instance.find_word('UQMIE'))
        self.assertEqual(True, boggle_instance.find_word('EIMQU'))
        self.assertEqual(True, boggle_instance.find_word('XRLF'))
        self.assertEqual(True, boggle_instance.find_word('SMG'))
        self.assertEqual(False, boggle_instance.find_word('AAGMSY'))
        self.assertEqual(False, boggle_instance.find_word('SMGG'))
        self.assertEqual(False, boggle_instance.find_word('SSMG'))


class HelperMethods:

    @staticmethod
    def configure_board_for_test(test_string, boggle_instance):
        string_array = HelperMethods.generate_string_array(test_string, boggle_instance.x_width, boggle_instance.y_width)
        return HelperMethods.map_string_array_to_board(string_array, boggle_instance)

    @staticmethod
    def generate_string_array(test_string, columns, rows):
        """
        :param test_string: A string that is rows*columns in length
        :param columns: The number of columns on the Board
        :param rows: The number of rows on the Board
        :return: An array of character arrays
        """
        string_array = []
        index = 0
        for i in range(rows):
            string_array.append([])
            for j in range(columns):
                string_array[i].append(test_string[index])
                index += 1
        return string_array

    @staticmethod
    def map_string_array_to_board(string_array, boggle_instance):
        """
        :param string_array: An array of character arrays (generated by HelperMethods.generate_string_array)
        :param boggle_instance: A Boggle object
        :return: A Boggle object whose Board's Space's Cube's top_letter parameters have been made to match
        corresponding values in letter_array
        """
        for r_idx, row in enumerate(boggle_instance.board.spaces):
            for c_idx, space in enumerate(row):
                space.cube.top_letter = string_array[r_idx][c_idx]
        return boggle_instance


class TestHelperMethods(unittest.TestCase):
    """
    This class inspects the Helper Methods for Boggle's unit tests.
    """

    def test_generate_string_array(self):
        test_string = 'abcdefghijklmnop'
        target = [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p']]
        self.assertEqual(HelperMethods.generate_string_array(test_string, 4, 4), target)

    def test_map_string_array_to_board(self):
        test_string = 'abcdefghijklmnop'
        string_array = HelperMethods.generate_string_array(test_string, 4, 4)
        boggle_instance = Boggle((4, 4), 1)
        boggle_instance_tl_mod = HelperMethods.map_string_array_to_board(string_array, boggle_instance)
        for r_idx, row in enumerate(string_array):
            for c_idx, column in enumerate(row):
                """
                The below test checks that each letter, in each row of string_array, matches the corresponding Space's
                Cube's top_letter parameter on the Board.
                """
                self.assertEqual(boggle_instance_tl_mod.board.spaces[r_idx][c_idx].cube.top_letter, string_array[r_idx][c_idx])


if __name__ == '__main__':
    unittest.main()
