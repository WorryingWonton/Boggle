class BoggleInterface:

    def __init__(self, game_instance):
        self.game_instance = game_instance

    def display_board(self):
        for row in self.game_instance.board.spaces:
            print(' '.join([x.cube.top_letter for x in row]))

    def display_scores(self):
        [print(f'{x.name}: {x.score}') for x in self.game_instance.players]

    def get_words(self, player):
        words = input(f'{player.name}, please enter all the words you can find in the above grid, separated by a space: ')
        return [word.lower() for word in words.split()]

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