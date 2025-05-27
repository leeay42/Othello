# Author: Ah Young Lee
# GitHub username: leeay42
# Date: 06/03/2023
# Description: Program that allows 2 people to play a text-based Othello game.
#               Has a Player class that initializes player object and
#               Othello class that initializes the board and keeps a dictionary
#               of player objects with methods that moves and flips the pieces,
#               tracks the score, updates the board, and returns the winner
#               when the game finishes.

class Player:
    """Represents a player in the game with a name and Othello game piece color.
    Used by the Othello class to initialize players"""
    def __init__(self, player_name, color):
        """Initializes the Player object with private data members for name and color.
        :parameter player_name - string for the name
        :parameter color - string for color of player game piece (black or white)"""
        self._player_name = player_name
        self._color = color

    def get_player_name(self):
        """returns player name. Used by Othello class to get the player's name"""
        return self._player_name

    def get_color(self):
        """returns color of player's game piece"""
        return self._color


class Othello:
    """Represents the game Othello as played by 2 players. Uses Player class to initialize
    the player objects. Has player dictionary of player objects and game board as private
    data members. Methods to play the game, track and change pieces on the board and
    return score and winner at the end."""
    def __init__(self):
        """Initializes Othello object with private data members board and players.
        Receives no parameters. Players are initialized as an empty dictionary.
        Board is initialized as a hard-coded 10x10 Othello game board ready for play
        with the following symbols:
            Edge: * (star)
            Black piece: X
            White piece: O
            Empty space: . """
        self._players = {}
        self._board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]

    def create_player(self, player_name, color):
        """Creates a new player using the Player class. Takes in 2 parameters:
        :parameter player_name - string for the name
        :parameter color - string for the color of the player's piece 'black' or 'white'
            and passes the 2 parameters to the Player class.
        Adds it to the players dictionary with the color as the key and
        the Player object as the value"""
        self._players[color] = Player(player_name, color)

    def print_board(self):
        """Prints out the current board by accessing data member board"""
        for row in self._board:
            print(*row)

    def count_black(self):
        """returns the number of black pieces on the board. Uses current board and
        a counter to track number of X's"""
        black = 0
        for row in self._board:
            for element in row:
                if element == "X":
                    black += 1
        return black

    def count_white(self):
        """returns the number of white pieces on the board. Uses current board and
        a counter to track number of O's"""
        white = 0
        for row in self._board:
            for element in row:
                if element == "O":
                    white += 1
        return white

    def return_winner(self):
        """Returns a statement regarding the outcome of the game. Pieces by color
        are counted by count_white() and count_black() method.
        Uses get_player_name method from Player class if there is a winner."""
        if self.count_white() > self.count_black():
            return "Winner is white player: " + self._players["white"].get_player_name()
        elif self.count_white() < self.count_black():
            return "Winner is black player: " + self._players["black"].get_player_name()
        else:
            return "It's a tie"

    def check_adjacent(self, opp_piece, row_coordinate, col_coordinate):
        """Returns list of opponent's pieces that are adjacent to empty space of interest
        as list of tuples.
        :parameter opp_piece - opponent piece ("X" or "O")
        :parameter row_coordinate - index of list of board
        :parameter col_coordinate - index of list of list of board
            row and col is position for specified empty space
        Uses board data member"""
        adj_opp_list = []
        shift = [-1, 0, 1]
        # empty space of interest and positions around it
        row_coord_list = [coord + row_coordinate for coord in shift]
        col_coord_list = [coord + col_coordinate for coord in shift]
        # row position around empty space
        for row_pos in row_coord_list:
            # column position around empty space
            for col_pos in col_coord_list:
                # if it is empty space itself
                if row_pos == row_coordinate and col_pos == col_coordinate:
                    continue
                # if the position around space has opponent's piece
                if self._board[row_pos][col_pos] == opp_piece:
                    adj_opp_list.append((row_pos, col_pos))
        return adj_opp_list

    def check_if_valid(self, opp_piece, row_coordinate, col_coordinate, adj_list):
        """Returns list of tuple locations of player's pieces that are at the end
        of opponent's pieces that are adjacent to empty space of interest
        as list of tuples
        :parameter opp_piece - opponent piece ("X" or "O")
        :parameter row_coordinate - index of list of board
        :parameter col_coordinate - index of list of list of board
            row and col is position for specified empty space
        :parameter adj_list - positions with opponent piece adjacent to empty space of interest
        Uses board data member"""
        end_color_list = []
        # each position with opponent piece
        for coord in adj_list:
            row, col = coord
            row_change = row - row_coordinate
            col_change = col - col_coordinate
            # while on the board, follow direction from empty space to adjacent opponent to end
            while row > 0 and row < 9 and col > 0 and col < 9:
                row = row + row_change
                col = col + col_change
                # contains player piece, add to list, stop
                if self._board[row][col] == opp_piece:
                    end_color_list.append((row, col))
                    break
                # empty space, stop
                if self._board[row][col] == ".":
                    break
        return end_color_list

    def return_available_positions(self, color):
        """Returns positions that are empty spaces with opponent's piece located adjacent to it
        and that following in that direction, ends uninterrupted to a player's piece
        :parameter 'color' which is either 'black' or 'white'
        Uses board data member and methods 'check_adjacent' and 'check_if_valid'
        to ascertain availability"""
        positions = []
        player_piece = ""
        opponent = ""
        if color == "black":
            player_piece = "X"
            opponent = "O"
        if color == "white":
            player_piece = "O"
            opponent = "X"
        # look at each position on board
        for ind, row in enumerate(self._board):
            for pos, element in enumerate(row):
                if element == '.':      # empty space
                    # check if opponent's piece is in adjacent location
                    adj_opp_list = self.check_adjacent(opponent, ind, pos)
                    # there is at least 1 adjacent opponent's piece
                    if adj_opp_list != []:
                        end_color_list = self.check_if_valid(player_piece, ind, pos, adj_opp_list)
                        # there is at least 1 route that starts at empty with adjacent opponent
                        # and ends with player piece
                        if end_color_list != []:
                            positions.append((ind, pos))
        return positions

    def flip_piece(self, player_piece, opp_piece, row_coordinate, col_coordinate, end_list):
        """Flips opponent's piece to player's piece in specified direction starting from
        empty space to adjacent opponent piece to end of player piece
        :parameter player_piece - player game piece ("X" or "O")
        :parameter opp_piece - opponent game piece ("X" or "O")
        :parameter row_coordinate - index of list of board
        :parameter col_coordinate - index of list of list of board
            row and col is position for specified empty space
        :parameter end_list - positions with player piece at the end of path
            starting from empty space of interest with opponent adjacent to it
        Uses board data member and methods 'check_adjacent' and 'check_if_valid' to
        get and change path from empty space to player end piece"""
        # each position that ends with player piece that starts at where placing new piece
        for coord in end_list:
            row, col = coord
            row_change = row_coordinate - row
            col_change = col_coordinate - col
            if row_change != 0:
                row_change = int(row_change/abs(row_coordinate - row))      # row direction
            if col_change != 0:
                col_change = int(col_change/abs(col_coordinate - col))      # column direction
            # while on the board, go down board in row-column direction
            while row > 0 and row < 9 and col > 0 and col < 9:
                row = row + row_change
                col = col + col_change
                # space has opponent piece, flip to player piece
                if self._board[row][col] == opp_piece:
                    self._board[row][col] = player_piece
                # space has player piece, stop
                elif self._board[row][col] == player_piece:
                    break

    def make_move(self, color, piece_position):
        """ Places player piece on board in specified empty space and flips rest of the
        necessary pieces to update the board. Then prints the board.
        :parameter color which is either 'black' or 'white'
        :parameter piece_position is tuple coordinates in board with (row, column) info,
            it is the empty position for player piece
        Uses board data member and methods 'check_adjacent' and 'check_if_valid' to
        get path from empty space to player end piece.  Then 'flip_piece' method
        changes the opponent's pieces to player's pieces in given path(s).
        'print_board' prints the changed board"""
        row, col = piece_position
        player_piece = ""
        opponent = ""
        if color == "black":
            player_piece = "X"
            opponent = "O"
        if color == "white":
            player_piece = "O"
            opponent = "X"
        # fill empty space with player piece
        self._board[row][col] = player_piece
        # get list of positions with opponent's piece adjacent to empty space
        adj_opp_list = self.check_adjacent(opponent, row, col)
        # empty space has at least 1 opponent's piece adjacent
        if adj_opp_list != []:
            end_color_list = self.check_if_valid(player_piece, row, col, adj_opp_list)
            # at least 1 direction of adjacent piece ends with player's piece
            if end_color_list != []:
                # flip pieces from starting position to end player piece
                self.flip_piece(player_piece, opponent, row, col, end_color_list)
        return self._board

    def play_game(self, color, piece_position):
        """Control center of the game. Takes in player color and where they want to
        place their game piece. Verifies if the position is valid or invalid.
        Moves the piece if valid and sends a statement with possible positions if invalid.
        If no more moves are possible for both players, sends a game over with points
        message and returns a statement with winner name.
        :parameter color which is either 'black' or 'white'
        :parameter piece_position is tuple coordinates in board with (row, column) info
        Uses 'return_available_positions' to check available moves for player and
        opponent. If none for either, uses 'return_winner' to get winner.  If move
        is valid, uses 'make_move' to move piece and change board. Invalid move does
        not use extra methods but makes a statement and shows possible moves from
        'return_available_positions'"""
        if color == "black":
            opponent = "white"
        else:
            opponent = "black"
        possible_positions = self.return_available_positions(color)
        # no possible positions
        if possible_positions == []:
            opponent_positions = self.return_available_positions(opponent)
            # opponent also has no possible positions
            if opponent_positions == []:
                # game end
                print("Game is ended white piece: ", self.count_white(),
                      "black piece: ", self.count_black())
                self.return_winner()
            # opponent has possible positions
            else:
                print("Here are the valid moves:", possible_positions)
                return "Invalid move"
        # position chosen is invalid
        elif piece_position not in possible_positions:
            print("Here are the valid moves:", possible_positions)
            return "Invalid move"
        # valid move
        elif piece_position in possible_positions:
            self.make_move(color, piece_position)

