class BoggleInterface:

    def __init__(self, game_instance):
        self.game_instance = game_instance

    def display_board(self):
        longest_face_len = self.find_longest_string()
        for row in self.game_instance.board.spaces:
            r_string = ''
            for space in row:
                r_string += space.cube.top_letter + ' ' * (longest_face_len - len(space.cube.top_letter) + 1)
            print(r_string)

    def find_longest_string(self):
        cur_longest = 0
        for row in self.game_instance.board.spaces:
            for space in row:
                cur_longest = max(len(space.cube.top_letter), cur_longest)
        return cur_longest

    def display_scores(self):
        [print(f'{x.name}: {x.score}') for x in self.game_instance.players]

    def get_words(self, player):
        words = input(f'{player.name}, please enter all the words you can find in the above grid, separated by a space: ')
        return [word.upper() for word in words.split()]

    def get_player_names(self):
        names = []
        print('Welcome to Boggle!')
        for i in range(self.game_instance.max_players):
            name = input(f'Player {i + 1}, what name would you like to use? ')
            names.append(name)
        return names

    def print_all_words(self, words):
        print(f'''All possible words: {words}
                  Total:  {len(words)}''')

    def display_final_scores(self):
        for player in self.game_instance.players:
            print(f'{player.name}: {player.score} - {player.words}')
