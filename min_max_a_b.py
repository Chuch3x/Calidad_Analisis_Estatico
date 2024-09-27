import copy
import time
from othello_utils import get_score, terminal_test, update_max_values, update_min_values, min_max_alpha_beta, get_min_max_move, play_othello_vs_ai, handle_ai_turn, handle_player_turn, get_player_input, display_game_result

N = 6
COUNTER = 0
EMPTY_CELL = 0
BLACK = 1
WHITE = -1

def initialize_board():
    board = [[EMPTY_CELL] * N for _ in range(N)]
    board[2][2] = BLACK
    board[2][3] = WHITE
    board[3][2] = WHITE
    board[3][3] = BLACK
    return board

def print_board(board):
    print("  0 1 2 3 4 5 ")
    for i in range(N):
        row = str(i) + " "
        for j in range(N):
            if board[i][j] == EMPTY_CELL:
                row += ". "
            elif board[i][j] == BLACK:
                row += "X "
            else:
                row += "O "
        print(row)

def is_valid_move(valid_moves, move):
    if move in valid_moves:
        return True
    return False

def get_player_tokens(board, player):
    player_tokens = []
    for row in range(N):
        for column in range(N):
            if board[row][column] == player:
                player_tokens.append((row, column))
    return player_tokens

def check_direction_for_valid_move(board, token, difference_row, difference_column, player):
    ady_row = token[0] + difference_row
    ady_col = token[1] + difference_column
    
    if 0 <= ady_row < N and 0 <= ady_col < N and board[ady_row][ady_col] == -player:
        while 0 <= ady_row < N and 0 <= ady_col < N and board[ady_row][ady_col] == -player:
            ady_row += difference_row
            ady_col += difference_column
            
        if 0 <= ady_row < N and 0 <= ady_col < N and board[ady_row][ady_col] == EMPTY_CELL:
            return (ady_row, ady_col)
    return None

def get_valid_moves(board, player):
    valid_moves = []
    for token in get_player_tokens(board, player):
        for difference_row in [-1, 0, 1]: 
            for difference_column in [-1, 0, 1]:
                if difference_row == 0 and difference_column == 0:
                    continue
                move = check_direction_for_valid_move(board, token, difference_row, difference_column, player)
                if move:
                    valid_moves.append(move)
    return valid_moves

def change_board(to_flip, player, board):
    for flip_row, flip_col in to_flip:
        board[flip_row][flip_col] = player   

def make_move(board, player, move):
    row = move[0]
    col = move[1]
    if not is_valid_move(get_valid_moves(board, player), move):
        return False
    board[row][col] = player
    for difference_row in [-1, 0, 1]:
        for difference_column in [-1, 0, 1]:
            if difference_row == 0 and difference_column == 0:
                continue
            new_row, new_column = row + difference_row, col + difference_column
            to_flip = find_flips_in_direction(board, player, new_row, new_column, difference_row, difference_column)
            if to_flip:
                change_board(to_flip, player, board)
    return True

def find_flips_in_direction(board, player, new_row, new_column, difference_row, difference_column):
    to_flip = []
    while 0 <= new_row < N and 0 <= new_column < N and board[new_row][new_column] == -player:
        to_flip.append((new_row, new_column))
        new_row += difference_row
        new_column += difference_column
    if 0 <= new_row < N and 0 <= new_column < N and board[new_row][new_column] == player:
        return to_flip
    return []

if __name__ == "__main__":
    opcion = 0
    print(" PLAYER VS IA")
    start_time = time.time()
    play_othello_vs_ai(initialize_board, print_board, get_valid_moves, make_move)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")