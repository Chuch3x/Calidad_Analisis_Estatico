import copy
import time
from othello_utils import is_valid_move, get_player_tokens, get_score, terminal_test, update_max_values, update_min_values, play_othello_vs_ai

board_size = 4
COUNTER = 0
EMPTY = 0
BLACK = 1
WHITE = -1

def initialize_board():
    board = [[EMPTY] * board_size for _ in range(board_size)]
    board[1][1] = BLACK
    board[1][2] = WHITE
    board[2][1] = WHITE
    board[2][2] = BLACK
    return board

def print_board(board):
    print("  0 1 2 3")
    for i in range(board_size):
        row = str(i) + " "
        for j in range(board_size):
            if board[i][j] == EMPTY:
                row += ". "
            elif board[i][j] == BLACK:
                row += "X "
            else:
                row += "O "
        print(row)


def get_valid_moves(board, player):
    valid_moves = set()
    for token in get_player_tokens(board, player, board_size):
        valid_moves.update(get_valid_moves_for_token(board, player, token))
    return list(valid_moves)

def get_valid_moves_for_token(board, player, token):
    valid_moves = []
    for direction in get_directions():
        move = find_valid_move_in_direction(board, player, token, direction)
        if move:
            valid_moves.append(move)
    return valid_moves

def get_directions():
    return [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]

def find_valid_move_in_direction(board, player, token, direction):
    dx, dy = direction
    x, y = token
    x += dx
    y += dy
    
    if not is_valid_position(x, y) or board[x][y] != -player:
        return None
    
    while is_valid_position(x, y) and board[x][y] == -player:
        x += dx
        y += dy
    
    if is_valid_position(x, y) and board[x][y] == EMPTY:
        return (x, y)
    return None

def is_valid_position(x, y):
    return 0 <= x < board_size and 0 <= y < board_size

def change_board(to_flip, player, board):
    for flip_row, flip_col in to_flip:
        board[flip_row][flip_col] = player

def make_move(board, player, move):
    row, col = move
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
    while 0 <= new_row < board_size and 0 <= new_column < board_size and board[new_row][new_column] == -player:
        to_flip.append((new_row, new_column))
        new_row += difference_row
        new_column += difference_column
    if 0 <= new_row < board_size and 0 <= new_column < board_size and board[new_row][new_column] == player:
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