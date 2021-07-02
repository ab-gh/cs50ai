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
        [(1, 0), (1, 1), (1, 2)], 
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
    alpha = -math.inf
    beta = math.inf
    def pruning(board, player, alpha, beta):
        # if end-game is reached
        if terminal(board):
            # return the board's utility
            return utility(board)
        elif player is X:
            # start low to work up
            v = -math.inf
            for action in actions(board):
                # choose the highest of the immediate options for this move
                v = max(v, pruning(result(board, action), O, alpha, beta))
                # replace alpha with v if v is higher
                alpha = max(alpha, v)
                # if above the beta threshold
                if alpha >= beta:
                    # value found
                    break
            return v
        elif player is O:
            v = math.inf
            for action in actions(board):
                v = min(v, pruning(result(board, action), X, alpha, beta))
                beta = min(beta, v)
                if alpha >= beta:
                    break
            return v

    if terminal(board):
        # End of Play
        move = None
    elif board is [[EMPTY]*3]*3:
        # Blank board, go for center
        move = (1, 1)
    if player(board) is X:
        # Start low to work up
        v = -math.inf
        for action in actions(board):
            # start searching down choices with alpha-beta pruning
            v_prime = pruning(result(board, action), O, alpha, beta)
            alpha = max(v, v_prime)
            if v_prime > v:
                v = v_prime
                move = action
    elif player(board) is O:
        v = math.inf
        for action in actions(board):
            v_prime = pruning(result(board, action), X, alpha, beta)
            beta = min(v, v_prime)
            if v_prime < v:
                v = v_prime
                move = action
    else:
        raise KeyboardInterrupt("Unexpected state.")
    return move

    
