"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None
    elif len([cell for row in board for cell in row if cell is X]) > len([cell for row in board for cell in row if cell is O]):
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_list = [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell is EMPTY]
    return set(action_list)

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    resultant = copy.deepcopy(board)
    if terminal(board):
        raise KeyboardInterrupt("Game over.")
    elif action not in actions(board):
        raise KeyboardInterrupt("This action is not a legal move.")
    resultant[i][j] = player(resultant)
    return resultant

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    runs = [
        # Horizontals
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 1)], 
        [(2, 0), (2, 1), (2, 2)],
        # Verticals
        [(0, 0), (1, 0), (2, 0)], 
        [(0, 1), (1, 1), (2, 1)], 
        [(0, 2), (1, 2), (2, 2)], 
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    for player in (X, O):
        for run in runs:
            if [board[i][j] for i, j in run] == [player] * 3:
                return player

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        # Win
        return True
    elif [cell for row in board for cell in row if cell is EMPTY]:
        # Ongoing
        return False
    else:
        # Draw
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
