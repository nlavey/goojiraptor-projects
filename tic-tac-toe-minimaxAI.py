import random
from random import choice

#@title Implementation of a Board class
class Board:
    ''' Implementation of a tic-tac-toe board class.
        A board is implemented as a dictionary, where keys are cell labels
        and values are cell marks 'X' or 'O' or empty ' '.'''

    def __init__(self):
        '''Sets an empty board.'''
        self.__board = {chr(65 + i) + str(j):' ' for i in range(3) for j in range(1, 4)}
        self.__winner = None

    @property
    def all_moves(self):
        return self.__board.keys()

    @property
    def valid_moves(self):
        '''Returns valid moves on the board that are empty cells.'''
        return [k for k in self.__board.keys() if self.isempty(k)]

    @property
    def winner(self):
        '''Returns the mark of the winner 'X', 'O', or None.'''
        return self.__winner

    def __setitem__(self, cell, mark):
        ''' Marks a cell with 'X' or 'O'.'''
        self.__board[cell.upper()] = mark.upper()

    def __getitem__(self, cell):
        '''Returns the mark of the cell.'''
        return self.__board[cell]

    def isempty(self, cell):
        ''' Returns True if the cell is empty.'''
        return self.__board[cell] == ' '

    @property
    def isdone(self):
        '''Returns True if one of the game terminating conditions is present.'''
        self.__winner = None
        if self.__board['A1'] == self.__board['B1'] == self.__board['C1'] != ' ':
            self.__winner = self.__board['A1']
            return True
        elif self.__board['A2'] == self.__board['B2'] == self.__board['C2'] != ' ':
            self.__winner = self.__board['A2']
            return True
        elif self.__board['A3'] == self.__board['B3'] == self.__board['C3'] != ' ':
            self.__winner = self.__board['A3']
            return True
        elif self.__board['A1'] == self.__board['A2'] == self.__board['A3'] != ' ':
            self.__winner = self.__board['A1']
            return True
        elif self.__board['B1'] == self.__board['B2'] == self.__board['B3'] != ' ':
            self.__winner = self.__board['B1']
            return True
        elif self.__board['C1'] == self.__board['C2'] == self.__board['C3'] != ' ':
            self.__winner = self.__board['C1']
            return True
        elif self.__board['A1'] == self.__board['B2'] == self.__board['C3'] != ' ':
            self.__winner = self.__board['A1']
            return True
        elif self.__board['A3'] == self.__board['B2'] == self.__board['C1'] != ' ':
            self.__winner = self.__board['A3']
            return True
        elif ' ' not in self.__board.values():
            # all cells filled → tie
            self.__winner = None
            return True
        else:
            return False


    def __repr__(self):
        '''Returns a string representation of the board.'''
        s = ''
        s +='   A   B   C\n'
        s +=' +---+---+---+\n'
        s += '{}| {} | {} | {} |\n'.format(1, self.__board['A1'], self.__board['B1'], self.__board['C1'])
        s +=' +---+---+---+\n'
        s += '{}| {} | {} | {} |\n'.format(2, self.__board['A2'], self.__board['B2'], self.__board['C2'])
        s +=' +---+---+---+\n'
        s += '{}| {} | {} | {} |\n'.format(3, self.__board['A3'], self.__board['B3'], self.__board['C3'])
        s +=' +---+---+---+\n'
        return s

    def show(self):
        '''Prints the board to the stdout (on the screen).'''
        print(self)

    def __iter__(self):
        '''Returns an iterator of the board.'''
        return iter(self.__board)

#@title Implementation of a Player class
class Player:
    '''Implementation of a tic-tac-toe Player class.'''
    def __init__(self, name, mark, board=None):
        '''Player's name and mark are required arguments. A board is optional.'''
        self.__name = name  # player's name
        self.__mark = mark  # player's mark is 'O' or 'X'
        self.__board = board

    @property
    def name(self):
        '''Returns the player's name.'''

        return self.__name

    @property
    def mark(self):
        '''Returns the player's mark.'''

        return self.__mark

    def choose(self, board):
        ''' Prompts the user to choose a cell.
        If the user enters a valid string and the cell on the board is empty, updates the board.
        Otherwise, prints a message that the input is wrong and reprints the prompt.'''

        while True:
            cell = input(f'{self.__name}, {self.__mark}: Enter a cell [A-C][1-3]:').upper()
            if cell in board.valid_moves:
                    ## YOUR CODE ##
                    board[cell] = self.__mark
                    break
            else:
                    print('You did not choose correctly.')

#@title Implementation of a tic-tac-toe game
print("Welcome to the TIC-TAC-TOE Game!")
while True:
    board = Board()
    player1 = Player("Bob", "X")
    player2 = Player("Alice", "O")
    turn = True
    while True:
        board.show()
        if turn:
            player1.choose(board)
            turn = False
        else:
            player2.choose(board)
            turn = True
        if board.isdone:
            break
    board.show()
    if board.winner == player1.mark:
        print(f"{player1.name} is the winner!")
    elif board.winner == player2.mark:
        print(f"{player2.name} is the winner!")
    else:
        print("It is a tie!")
    ans = input("Would you like to play again? [Y/N]\n").upper()
    if (ans != "Y"):
        break
print("Goodbye!")

class AI(Player):
    '''Implementation of a tic-tac-toe AI player class.'''
    def __init__(self, name, mark, board=None):
        super().__init__(name, mark, board)

    @property
    def opponent_mark(self):
        '''Returns the opponent's mark.'''
        if self.mark.upper() == 'X':
          return 'O'
        else:
          return 'X'


    def nextmove(self, board):
        '''Returns the next player's move.'''
        return choice(board.valid_moves)

    def choose(self, board):
        '''Prints the prompt and the player's move and marks the cell on the board.'''
        cell = self.nextmove(board)
        board[cell] = self.mark
        print(f'{self.name}, {self.mark}: Enter a cell [A-C][1-3]: {cell}')

#@title Implementation of a MiniMax class
import copy
class MiniMax(AI):
    '''Implementation of a tic-tac-toe MiniMax AI class based on a minimax algorithm.'''
    def __init__(self, name, mark, board=None):
        super().__init__(name, mark, board)

    def nextmove(self, board):
        '''Returns the next player's move.'''
        return self.minimax(board, True, True)

    def minimax(self, board, isplayer, start):
        '''Returns a valid player's move.'''
        if board.isdone:                  # check the base condition
            if board.winner == self.mark: # the player won the game
                return 1
            elif board.winner == None:    # the game is a tie
                return 0
            else:
                return -1                 # the player lost the game

        maxscore, minscore = -10, 10
        bestmove = None
        # Make a move recursively.

        for valid_move in board.valid_moves:
          score = 0
          copy_board = copy.deepcopy(board)
          if isplayer:
              copy_board[valid_move] = self.mark
              score += self.minimax(copy_board, not isplayer, False)
              #board[valid_move] = ' '
              if score > maxscore:
                maxscore = score
                bestmove = valid_move
          else:
              copy_board[valid_move] = self.opponent_mark
              score += self.minimax(copy_board, not isplayer, False)
              #board[valid_move] = ' '
              if score < minscore:
                minscore = score
                bestmove = valid_move



        if start:
            return bestmove
        elif isplayer:
            return maxscore
        else:
            return minscore
        
#@title Implementation of a SmartAI class
class SmartAI(AI):
    '''Implementation of a SmartAI class.'''

    def nextmove(self, board):
        '''Returns the next player's move.'''
        # Step 1: block opponent if they’re about to win
        win_lines = [
            ['A1', 'A2', 'A3'],
            ['B1', 'B2', 'B3'],
            ['C1', 'C2', 'C3'],
            ['A1', 'B1', 'C1'],
            ['A2', 'B2', 'C2'],
            ['A3', 'B3', 'C3'],
            ['A1', 'B2', 'C3'],
            ['A3', 'B2', 'C1']
        ]

        for line in win_lines:
            cells = [board[pos] for pos in line]
            if cells.count(self.opponent_mark) == 2 and cells.count(' ') == 1:
                return line[cells.index(' ')]

        # Step 2: take center if available
        if 'B2' in board.valid_moves:
            return 'B2'

        # Step 3: pick a corner
        corners = ['A1', 'A3', 'C1', 'C3']
        valid_corners = [c for c in corners if c in board.valid_moves]
        if valid_corners:
            return choice(valid_corners)

        # Step 4: pick an edge
        edges = ['A2', 'B1', 'B3', 'C2']
        valid_edges = [e for e in edges if e in board.valid_moves]
        if valid_edges:
            return choice(valid_edges)

        # Step 5: fallback
        return choice(board.valid_moves)
        
#@title Implementation of a tic-tac-toe game with SmartAI and MiniMax
score_player1, score_player2, score_tie = 0, 0, 0
for i in range(5):
    board = Board()
    player1 = MiniMax("Max", "X")
    player2 = SmartAI("Alice", "O")
    turn = True
    while True:
        board.show()
        if turn:
            player1.choose(board)
            turn = False
        else:
            player2.choose(board)
            turn = True
        if board.isdone:
            break
    board.show()
    if board.winner == player1.mark:
        score_player1 += 1
    elif board.winner == player2.mark:
        score_player2 += 1
    else:
        score_tie += 1
print(f'{player1.name} won {score_player1} games.')
print(f'{player2.name} won {score_player2} games.')
print(f'There are {score_tie} tied games.')
