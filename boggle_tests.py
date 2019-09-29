import unittest
from boggle import Boggle
from itertools import permutations

"""
I want to fully validate my Boggle code.
I should test:
    -There is a way to verify is a word is correct per the rules of Boggle for a variety of board sizes, aspect ratios and alphabets
    -There is a mechanism for verifying that a word is valid english, and that said word is scored according to a pre-supplied model
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
        -Rectangular Board behavior
            -2x2
            -2x(n + 2)
            -(n + 2)x2
            -3x3
            -3x(n + 3)
            -(n + 3)x3
        -A word can be found using a combination of horizontal, vertical, and diagonal moves
        -A word will not be counted if it uses the same letter on the board more than once
        -A word will not be counted if part of it is not on the board
    """
    def test_single_letter_board(self):
        test_string = 'A'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((1, 1), 1, dictionary='test_words.txt'))
        self.assertEqual(True, boggle_instance.find_word(test_string))

    def test_find_single_letter_amongst_many(self):
        test_string = 'ABCDEFGHIJKLMNOP'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((4, 4), 1, dictionary='test_words.txt'))
        for char in test_string:
            self.assertEqual(True, boggle_instance.find_word(char))

    def test_find_multi_character_top_letter(self):
        boggle_instance = TestableBoggle((5, 5), 1, dictionary='test_words.txt')
        boggle_instance.board.spaces[2][4].cube.top_letter = 'Quack'
        self.assertEqual(True, boggle_instance.find_word('QUACK'))

    def test_find_horizontal_letters(self):
        """Uses a 1 x 10 board
            -Checks left to right
            -Checks right to left
            -Verifies a word must be fully on the board
        """
        test_string = 'abcdefghij'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((10, 1), 1, dictionary='test_words.txt'))
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
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((1, 10), 1, dictionary='test_words.txt'))
        self.assertEqual(True, boggle_instance.find_word(test_string.upper()))
        self.assertEqual(True, boggle_instance.find_word('DEF'))
        self.assertEqual(False, boggle_instance.find_word('CC'))
        self.assertEqual(False, boggle_instance.find_word('GHIJJ'))
        self.assertEqual(False, boggle_instance.find_word('AABC'))

    def test_find_diagonal_letters(self):
        test_string = 'abcdefghijklmnopqrstuvwxy'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((5, 5), 1, dictionary='test_words.txt'))
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

    def test_find_multi_directional_arrangements(self):
        test_string = 'aabbccddeeffgghhiijjkkllm'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((5, 5), 1, dictionary='test_words.txt'))
        # [['a', 'a', 'b', 'b', 'c'],
        #  ['c', 'd', 'd', 'e', 'e'],
        #  ['f', 'f', 'g', 'g', 'h'],
        #  ['h', 'i', 'i', 'j', 'j'],
        #  ['k', 'k', 'l', 'l', 'm']]
        self.assertEqual(True, boggle_instance.find_word('ADDAB'))
        self.assertEqual(True, boggle_instance.find_word('ADDBA'))
        self.assertEqual(True, boggle_instance.find_word('FIIGEG'))
        self.assertEqual(True, boggle_instance.find_word('AABBCEEHGIJMLLIKHFC'))
        self.assertEqual(False, boggle_instance.find_word('AABBCEEHGIJMLLIKHFCA'))
        self.assertEqual(False, boggle_instance.find_word('AABBCEEHGIJMLLIKHFCM'))
        self.assertEqual(False, boggle_instance.find_word('AABBCC'))
        self.assertEqual(False, boggle_instance.find_word('AABBB'))

    def test_2x2(self):
        test_string = 'ABCD'
        test_words = sum([[''.join(x) for x in list(permutations(test_string, r=r))] for r in range(1, 5)], [])
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((2, 2), 1, dictionary='test_words.txt'))
        for word in test_words:
            self.assertEqual(True, boggle_instance.find_word(word))
        self.assertEqual(False, boggle_instance.find_word('ABDD'))
        self.assertEqual(False, boggle_instance.find_word('DABA'))

    def test_10x2(self):
        test_string = 'aabbccddeeffgghhiijj'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((10, 2), 1, dictionary='test_words.txt'))
        # [['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd', 'e', 'e'],
        #  ['f', 'f', 'g', 'g', 'h', 'h', 'i', 'i', 'j', 'j']]
        self.assertEqual(True, boggle_instance.find_word('AABBCCDDEEJJIIHHGGFF'))
        self.assertEqual(True, boggle_instance.find_word('AFFABGGBCHHCDIIDEJJE'))
        self.assertEqual(True, boggle_instance.find_word('AFFABGGBCHHCIDIDEJEJ'))
        self.assertEqual(False, boggle_instance.find_word('AAGFFB'))
        self.assertEqual(False, boggle_instance.find_word('AAGGF'))
        self.assertEqual(False, boggle_instance.find_word('AAGGBBFFF'))

    def test_2x10(self):
        test_string = 'abcdefghijklmnopqrst'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((2, 10), 1, dictionary='test_words.txt'))
        # [['a', 'b'],
        #  ['c', 'd'],
        #  ['e', 'f'],
        #  ['g', 'h'],
        #  ['i', 'j'],
        #  ['k', 'l'],
        #  ['m', 'n'],
        #  ['o', 'p'],
        #  ['q', 'r'],
        #  ['s', 't']]
        self.assertEqual(True, boggle_instance.find_word('ACEGIKMOQSTRPNLJHFDB'))
        self.assertEqual(True, boggle_instance.find_word(test_string.upper()))
        self.assertEqual(True, boggle_instance.find_word('ACBDEHFGJILKNPMORSTQ'))
        self.assertEqual(False, boggle_instance.find_word('CBDAEHFGJILKNPMORSTQ'))
        self.assertEqual(False, boggle_instance.find_word('ACBDEHFGJILKNPMORSTQS'))

    def test_3x3(self):
        test_string = 'abcdefghi'
        boggle_instance = HelperMethods.configure_board_for_test(test_string, TestableBoggle((3, 3), 1, dictionary='test_words.txt'))
        self.assertEqual(True, boggle_instance.find_word('ABCFEDGHI'))
        self.assertEqual(True, boggle_instance.find_word('EABCFIHG'))
        self.assertEqual(False, boggle_instance.find_word('IHGA'))
        self.assertEqual(False, boggle_instance.find_word('IHGC'))
        self.assertEqual(False, boggle_instance.find_word('IHGG'))

    def test_10x3(self):
        test_stirng = 'abcdefghijklmnopqrst0123456789'
        # [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
        #  ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'],
        #  ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
        boggle_instance = HelperMethods.configure_board_for_test(test_stirng, TestableBoggle((10, 3), 1, dictionary='test_words.txt'))
        self.assertEqual(True, boggle_instance.find_word('abcdefghijsrqponmlk0123456789'.upper()))
        self.assertEqual(True, boggle_instance.find_word('LAK012MCB'))
        self.assertEqual(True, boggle_instance.find_word('DOPEN3'))
        self.assertEqual(False, boggle_instance.find_word('DOPEN5'))

    def test_3x10(self):
        test_stirng = 'abcdefghijklmnopqrst0123456789'
        # [['a', 'b', 'c'],
        #  ['d', 'e', 'f'],
        #  ['g', 'h', 'i'],
        #  ['j', 'k', 'l'],
        #  ['m', 'n', 'o'],
        #  ['p', 'q', 'r'],
        #  ['s', 't', '0'],
        #  ['1', '2', '3'],
        #  ['4', '5', '6'],
        #  ['7', '8', '9']]
        boggle_instance = HelperMethods.configure_board_for_test(test_stirng, TestableBoggle((3, 10), 1, dictionary='test_words.txt'))
        self.assertEqual(True, boggle_instance.find_word('ADGJMPS147852TQNKHEBCFILOR0369'))
        self.assertEqual(True, boggle_instance.find_word('AEIKMQ024'))
        self.assertEqual(True, boggle_instance.find_word('NLKJMPQRO'))
        self.assertEqual(False, boggle_instance.find_word('LKNOP'))
        self.assertEqual(False, boggle_instance.find_word('AADE'))


class TestIfValidEnglish(unittest.TestCase):

    def test_if_valid_english(self):
        """
        Tests that Boggle will accept words that are valid english and above the minimum length (as set by the scoring model)
        Note:  My code will not accept words with more letters than there are spaces on the Board.
        :return:
        """
        valid_words = ['obsequious', 'sycophantic', 'obese', 'pigeon', 'hole', 'pigeonholed', 'and', 'onomatopoeia']
        invalid_words = ['am', 'to', 'me', 'i', 'a', 'an', 'meldspar']
        boggle_instance = TestableBoggle((10, 10), 1, dictionary='boggle_words.txt', scoring_model=[(0, 0), (3, 1), (4, 1), (5, 2), (6, 3), (7, 5), (8, 11)])
        for word in valid_words:
            self.assertEqual(True, boggle_instance.check_if_valid_english(word))
        for word in invalid_words:
            self.assertEqual(False, boggle_instance.check_if_valid_english(word))


class TestScoringSystem(unittest.TestCase):
    """
    This verifies two pieces of functionality relating to scoring words:
        1.  Words are scored correctly based on the scoring model supplied.
        2.  The same word supplied by two or more players during a round will not count towards any of their scores.
    """
    def test_word_scoring(self):
        boggle_instance = TestableBoggle((10, 10), 1, dictionary='test_words.txt', scoring_model=[(0, 0), (3, 1), (4, 1), (5, 2), (6, 3), (7, 5), (8, 11)])
        test_strings = {'': 0, '1': 0, '12': 0, '123': 1, '1234': 1, '12345': 2, '123456': 3, '1234567': 5, '12345678': 11, '123456789': 11}
        for word in test_strings.keys():
            self.assertEqual(test_strings[word], boggle_instance.score_word(word))

    def test_round_scoring(self):
        pass


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
        boggle_instance = TestableBoggle((4, 4), 1, dictionary='test_words.txt')
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
