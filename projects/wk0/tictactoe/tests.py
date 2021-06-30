from tictactoe import initial_state, player, actions, result, winner, terminal

X = "X"
O = "O"
EMPTY = None

def board():
    #return [[EMPTY, EMPTY, EMPTY],
    #        [EMPTY, X, O],
    #        [EMPTY, EMPTY, EMPTY]]

    return [[X, O, X],
            [O, X, O],
            [O, X, O]]

if __name__ == "__main__":
    #print(player(initial_state()))
    #print(actions(initial_state()))
    #print(result(initial_state(), (0, 1)))
    #print(winner(board()))
    print(terminal(board()))

