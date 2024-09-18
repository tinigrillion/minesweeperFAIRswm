"""
Implementation of command-line minesweeper by Kylie Ying
Github: https://www.github.com/kying18

Modified.
"""

import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        """Creates a board object that represents the minesweeper game.

        :param dim_size: Size of the board.
        :type dim_size: int
        :param num_bombs: Number of planted bombs.
        :type num_bombs: int
        """
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we'll save (row,col) tuples into this set 
        self.dug = set() # if we dig at 0, 0, then self.dug = {(0,0)}

    def make_new_board(self):
        """Constructs the new board and plants the bombs.

        The board is an array like this:
        |  [[None, None, ..., None],
        |  [None, None, ..., None],
        |  [...                  ],
        |  [None, None, ..., None]]
        |  Random positions of the array are populated with "*", representing bombs.

        :returns: The board array.
        :rtype: List of lists
        """
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) # return a random integer N such that a <= N <= b
            row = loc // self.dim_size  # we want the number of times dim_size goes into loc to tell us what row to look at
            col = loc % self.dim_size  # we want the remainder to tell us what index in that row to look at

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue

            board[row][col] = '*' # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        """This docstring needs editing!"""
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        """Counts the number of neighbouring bombs in each position of the board that does not contain a bomb.

        Each position with coordinates (row,col) has following neighbours:
        top left: (row-1, col-1)
        top middle: (row-1, col)
        top right: (row-1, col+1)
        left: (row, col-1)
        right: (row, col+1)
        bottom left: (row+1, col-1)
        bottom middle: (row+1, col)
        bottom right: (row+1, col+1)

        :param row: Row coordinate of examined position.
        :param col: Column coordinate of examined position.
        :return: The number of neighbouring bombs
        :rtype: int
        """
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        """Start digging a position and return whether *no* bomb has been hit

        :param row: Row coordinate of position to dig.
        :param col: Column coordinate of position to dig.
        :return: Whether *no* bomb as been hit
        :rtype: Boolean
        """

        self.dug.add((row, col)) # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # don't dig where you've already dug
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we *shouldn't* hit a bomb here
        return True

    def __str__(self):
        """This docstring needs editing!"""
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# play the game
def play(dim_size=10, num_bombs=10):
    """Plays the minesweeper game.

    |  Step 1: Creates the board and plant the bombs
    |  Step 2: Shows the user the board and asks where they want to dig
    |  Step 3a: If location is a bomb, shows game over message
    |  Step 3b: If location is not a bomb, digs recursively until each square is at least next to a bomb
    |  Step 4: Repeats steps 2 and 3a/b until there are no more places to dig -> VICTORY!

    :param dim_size: Size of the board. (default: 10)
    :type dim_size: int
    :param num_bombs: Number of planted bombs. (default: 10)
    :type num_bombs: int
    """
    board = Board(dim_size, num_bombs)
    safe = True 

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # 0,0 or 0, 0 or 0,    0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhhh
            break # (game over rip)

    # 2 ways to end loop, lets check which one
    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        # let's reveal the whole board!
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': # good practice :)
    play()
