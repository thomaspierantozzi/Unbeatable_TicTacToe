import numpy as np
from itertools import product

class Game_Manager():
    '''
    class which manages the game and the instances of the objects
    sub-class of the object type
    '''

    def __init__(self):
        self.welcome_message()
        self.players_list = [
            Player(player_nr=1),
            Player(player_nr=2)
        ]
        self.__refresh_grid()
        self.nr_moves:int = 0
        self.winning_condition = False

    def welcome_message(self):
        print("""
         __    __     _                            _        
        / / /\ \ \___| | ___ ___  _ __ ___   ___  | |_ ___  
        \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
         \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |
         _____\_ \___|_|________/|_| |_| |______|  \__\___/ 
        /__   (_) ___  /__   \__ _  ___  /__   \___   ___   
          / /\/ |/ __|   / /\/ _` |/ __|   / /\/ _ \ / _ \  
         / /  | | (__   / / | (_| | (__   / / | (_) |  __/  
         \/   |_|\___|  \/   \__,_|\___|  \/   \___/ \___|  
         
         Try to beat me if you can...
         
         v.0.1 - by Thomas Pierantozzi
        """)

    def __refresh_grid(self) -> None:
        """
        method to print the grid on the terminal window based on the status held in the players' tiles_chosen
        :param self:
        :return: None
        """
        grid_status = np.zeros(shape=(3, 3))
        #making a sum of a neutral grid with the tiles chosen by every player. This way we have a grid withe choices
        #made by everyone
        for player in self.players_list:
            grid_status += player.tiles_chosen

        #print the grid
        print ('\n\n\n')
        for row in range(3):
            print(f'{self.__check_squares(square=(row, 0)):^5}|'
                  f'{self.__check_squares(square=(row, 1)):^5}|'
                  f'{self.__check_squares(square=(row, 2)):^5}')
            if row != 2:
                print('------------------')

    def __check_squares(self, square) -> str:
        """
        method to check whether a tile has been chosen by the p1, p2 or none of them.
        Based on the fact that, this specific squares belongs to a player, the method return X, O (or '' in case
        the tile is not belonging to anyone)
        :param square: tuple pointing to a specific square (following numpy indexing order)
        :return: string to be printed on the terminal grid
        """
        for player in self.players_list:
            if player.tiles_chosen[square] != 0:
                return 'X' if player == self.players_list[0] else 'O'
        return ''

    def choose_a_tile(self, player) -> bool:
        """
        method to let the player choose a tile on their turn
        :param player: instance of player1 or player2
        :return: boolean value. True if the move is allowed, otherwise False
        """
        choice: str = input (f'Please, {player.name}, pick your tile\n'
                               f'(input x,y where x is the row and y is the column chosen):\n\t\t')
        choice: tuple = tuple([int(item) for item in choice.split(',') if item.isnumeric()])
        if self.__is_move_valid(choice):
            player.tiles_chosen[choice[0],choice[1]] = 1 if player == self.players_list[0] else 2
            self.__refresh_grid()
            self.__check_victory(player)
            return True
        else:
            print ('++++ Invalid move... +++++')
            return False
    #TODO 1: CLOSE the choose a tile method

    def __is_move_valid(self, square: tuple) -> bool:
        """
        method to check if a chosen tile is a valid move or not
        :param square: tuple pointing to a specific square (following numpy indexing order)
        :return: boolean value. True if the move is allowed, otherwise False
        """
        if square in product (range(3), range(3)):
            is_tile_taken = (self.players_list[0].tiles_chosen[square[0],square[1]],
                             self.players_list[1].tiles_chosen[square[0],square[1]])
            return not (is_tile_taken[0] or is_tile_taken[1]) #finchè sono entrambe False, is_move_valid è True
        else:
            return False

    def __check_victory(self, player) -> bool:
        """
        method to check whether a player has a won or not
        :param player: instance of player1 or player2
        :return: boolean value. True if the player has won, otherwise False
        """
        for row in range(3):
            row = player.tiles_chosen[row,:]
            if row.sum() % 3 == 0 and row.sum() != 0:
                self.winning_condition = True
        for column in range(3):
            column = player.tiles_chosen[:,column]
            if column.sum() % 3 == 0 and column.sum() != 0:
                self.winning_condition = True
        diagonal_main = player.tiles_chosen.diagonal().sum()
        if diagonal_main % 3 == 0 and diagonal_main != 0:
            self.winning_condition = True
        diagonal_sec = player.tiles_chosen[0,2] + player.tiles_chosen[1,1] + player.tiles_chosen[2,0]
        if diagonal_sec % 3 == 0 and diagonal_sec != 0:
            self.winning_condition = True

    def restart_game(self):
        """
        method to restart the game and have all the objects cleaned for a new game
        :return: None
        """
        for player in self.players_list:
            player.clean_player()
        self.winning_condition = False
        self.__refresh_grid()

class Player():
    """
    object which holds the attributes and methods for the single player
    """

    def __init__(self, player_nr: int):
        self.player_nr = player_nr
        self.name = input(f'Please insert name for player-{self.player_nr:02}:\n\t\t')
        self.CPU = False
        choice = input('Is this player a CPU? (Y/N):\n\t\t')
        if choice.lower() == 'y' or choice.lower == 'yes':
            self.CPU = True
        self.tiles_chosen = np.zeros(shape=(3, 3))  #the grid is empty for the moment, no tiles belong to give player

    def clean_player(self):
        """
        method to clean all of the data stored in a player's instance, in order to start another match
        :return: None
        """
        self.tiles_chosen = np.zeros(shape=(3, 3))


if __name__ == '__main__':
    gm = Game_Manager()
    while gm.winning_condition == False:
        valid_move = False
        current_player = gm.players_list[0] if gm.nr_moves % 2 == 0 else gm.players_list[1]
        while valid_move == False:
            valid_move = gm.choose_a_tile(current_player)
            if valid_move:
                gm.nr_moves += 1
        if gm.winning_condition:
            print (f'\n\n\n'
                   f'********************************************************\n'
                   f'{current_player.name} won!\n'
                   f'********************************************************')

            choice = input ('Do you want to play again? (Y/N):')
            if choice.lower() == 'y' or choice.lower == 'yes':
                gm.restart_game()