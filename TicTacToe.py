import numpy as np
from itertools import product, cycle
from random import choice
import sys

#i define the value of the cells, based on the number of potential winning possibilities
TIER1 = [(1,1)]
TIER2 = [(0,0),
         (0,2),
         (2,0),
         (2,2)]
TIER3 = [(0,1),
         (1,0),
         (1,2),
         (2,1)]


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
        if player.CPU == False:
            choice: str = input (f'Please, {player.name}, pick your tile\n'
                                   f'(input x,y where x is the row and y is the column chosen):\n\t\t')
            choice: tuple = tuple([int(item) for item in choice.split(',') if item.isnumeric()])
        else:
            av_squares = self.squares_available()
            choice = player.CPU_choice(available_squares=av_squares)
        if self.__is_move_valid(choice):
            player.tiles_chosen[choice[0],choice[1]] = 1 if player == self.players_list[0] else 2
            self.__refresh_grid()
            self.__check_victory(player)
            return True
        else:
            print ('++++ Invalid move... +++++')
            return False

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

        #TODO 1: IL SISTEMA RIMANE BLOCCATO SULLA SCELTA DELLA MOSSA SULLE DIAGONALI, A VOLTE. RIVEDERE IL SISTEMA DI SCELTA.

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

        choice = input('Do you want to play again? (Y/N):')
        if choice.lower() == 'y' or choice.lower == 'yes':
            for player in self.players_list:
                player.clean_player()
            self.winning_condition = False
            self.__refresh_grid()
            self.nr_moves = 0
        else:
            sys.exit('Game Over')

    def squares_available(self) -> list:
        """
        returns a list of valid choices to pick
        :return: list of valid choices to pick
        """
        player1 = self.players_list[0]
        player2 = self.players_list[1]
        p1_left_free = [(item[0], item[1]) for item in zip (np.where(player1.tiles_chosen == 0)[0], np.where(player1.tiles_chosen == 0)[1])]
        p2_left_free = [(item[0], item[1]) for item in zip (np.where(player2.tiles_chosen == 0)[0], np.where(player2.tiles_chosen == 0)[1])]

        return [value for value in p1_left_free if value in p2_left_free]



class Player():
    __player_list = list ()
    """
    object which holds the attributes and methods for the single player
    """
    def __new__ (cls, player_nr):
        instance = super().__new__(cls)
        cls.__player_list.append(instance)
        return instance

    def __init__(self, player_nr: int):
        self.player_nr = player_nr
        self.name = input(f'Please insert name for player-{self.player_nr:02}:\n\t\t')
        self.CPU = False
        if self.player_nr == 2:
            choice = input('Is this player a CPU? (Y/N):\n\t\t')
            if choice.lower() == 'y' or choice.lower == 'yes':
                self.CPU = True
        self.tiles_chosen = np.zeros(shape=(3, 3))  #the grid is empty for the moment, no tiles belong to give player

    def __repr__(self):
        return f'Player: {self.name:>15}'

    def clean_player(self):
        """
        method to clean all of the data stored in a player's instance, in order to start another match
        :return: None
        """
        self.tiles_chosen = np.zeros(shape=(3, 3))

    def print_choice (func, *args, **kwargs):
        def wrapper (*args, **kwargs):
            output = func (*args, **kwargs)
            print (f'{func.__name__} : {output}')
            return output
        return wrapper

    @print_choice
    def CPU_choice (self, available_squares) -> tuple:
        """
        method to pick a square from the remaining and try to win the game
        :param available_squares: list of available squares
        :return: tuple containing the square picked
        """
        #if the central square has not been taken yet, then the choice must be that one no matter what
        if ((1,1) in available_squares):
            return (1,1)
        winning_square = self.__can_cpu_wins(available_squares = available_squares)
        if winning_square != None:
            return winning_square
        can_the_opponent_win = self.__can_the_opponent_win(available_squares = available_squares)
        if can_the_opponent_win:
            return can_the_opponent_win

        #if none of the previos conditions is met then
        return self.__pick_a_square(available_squares = available_squares)

    @print_choice
    def __can_cpu_wins (self, available_squares) -> tuple:
        """
        method to check whether the CPU can win with the upcoming move
        :return: tuple containing the win condition.
        """
        for row_nr in range(3):
            row = self.tiles_chosen[row_nr, :]
            if row.sum() == 4:
                chosen_value = (row_nr, np.where (row == 0)[0])
                if chosen_value in available_squares:
                    return chosen_value
        for column_nr in range(3):
            column = self.tiles_chosen[:, column_nr]
            if column.sum() == 4:
                chosen_value = (np.where (column == 0)[0], column_nr)
                if chosen_value in available_squares:
                    return chosen_value
        diagonal_main = self.tiles_chosen.diagonal().sum()
        if diagonal_main == 4:
            for tuple in [(0,0), (2,2)]: #for sure it is a square on the corner since the mid one will be kept on the second move at most
                if tuple in available_squares:
                    return tuple
        diagonal_sec = self.tiles_chosen[0, 2] + self.tiles_chosen[1, 1] + self.tiles_chosen[2, 0]
        if diagonal_sec == 4:
            return (0,2) if self.tiles_chosen[0, 2] == 0 else (2,0)
        return None

    @print_choice
    def __can_the_opponent_win(self, available_squares) -> tuple:
        """
        method to pick a square from the ones available and with the goal of blocking the opponent's possibilities to win
        :param available_squares: list of available squares
        :return: tuple containing the square picked
        """
        #since the human player can only be the player1 when a CPU is challenged
        opponent_squares = self.__player_list[0].tiles_chosen

        for row_nr in range(3):
            row = opponent_squares[row_nr, :]
            if row.sum() == 2:
                chosen_value = (row_nr, np.where (row == 0)[0])
                if chosen_value in available_squares:
                    return chosen_value
        for column_nr in range(3):
            column = opponent_squares[:, column_nr]
            if column.sum() == 2:
                chosen_value = (np.where (column == 0)[0], column_nr)
                if chosen_value in available_squares:
                    return chosen_value
        diagonal_main = opponent_squares.diagonal().sum()
        if diagonal_main == 2:
            for tuple in [(0,0), (2,2)]: #for sure it is a square on the corner since the mid one will be kept on the second move at most
                if tuple in available_squares:
                    return tuple
        diagonal_sec = opponent_squares[0, 2] + opponent_squares[1, 1] + opponent_squares[2, 0]
        if diagonal_sec == 2:
            for tuple in [(0,2), (2,0)]:
                return tuple if tuple in available_squares else None
        return None


    @print_choice
    def __pick_a_square(self, available_squares) -> tuple:
        '''
        This method covers only the first move. Since only on the first turn up to the CPU there are no ways to win with
        an upcoming move.
        It chooses one of the 4 corners since these are the squares most valuable after the central one (which is selected
        as a first move in case the opponent should leave it unchosen on the opening pick)
        :return : tuple containing the square picked
        '''

        list_of_choices = [item for item in TIER2 if item in available_squares]
        return choice(list_of_choices)


if __name__ == '__main__':
    gm = Game_Manager()
    player_generator = cycle(gm.players_list) #generator used below to get the current player to move
    while gm.winning_condition == False and gm.nr_moves < 9:
        valid_move = False

        #from the generator here above I cycle through the players and everytime i get the current one
        current_player = next (player_generator)
        while valid_move == False:
            valid_move = gm.choose_a_tile(current_player)
            if valid_move:
                gm.nr_moves += 1
        if gm.winning_condition:
            print (f'\n\n\n'
                   f'********************************************************\n'
                   f'{current_player.name} won!\n'
                   f'********************************************************')

            gm.restart_game()
        if gm.nr_moves == 9:
            print (f'\n\n\n'
                   f'********************************************************\n'
                   f'{gm.players_list[0].name} your match ended up in a draw with {gm.players_list[1].name}...\n'
                   f'you couldn\'t do any better... ain\'t you ?!?\n'
                   f'********************************************************')
            gm.restart_game()