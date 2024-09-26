import copy
import time
from othello_utils import is_valid_move, get_player_tokens, get_score, terminal_test, update_max_values, update_min_values

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

def min_max_alpha_beta(board, player, alpha, beta, maximizing_player):
    global COUNTER
    COUNTER += 1
    if terminal_test(board, EMPTY):
        return get_score(board, BLACK, WHITE)[1], 0
    
    valid_moves = get_valid_moves(board, player)
    if maximizing_player:
        max_val = float('-inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, player, move)
            evaluation, best_move = min_max_alpha_beta(new_board, player, alpha, beta, False)
            
            max_val, best_move = update_max_values(evaluation, max_val, move, best_move)

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, -player, move)
            evaluation, best_move = min_max_alpha_beta(new_board, player, alpha, beta, True)

            min_val, best_move = update_min_values(evaluation, min_val, move, best_move)

            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_val, best_move
    
def get_min_max_move(board, player):
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) > 0:
        _, best_move= min_max_alpha_beta(board, player, float('-inf'), float('inf'), False)
        print("IA move: ", best_move)
        if best_move == 0:
            return get_valid_moves(board, player)[0]
        else:
            return best_move
    else:
        return (-1, -1)

def play_othello_vs_ai():
    board = initialize_board()
    current_player = BLACK
    while not terminal_test(board, EMPTY):
        print_board(board)
        print("Actual player:", "X" if current_player == BLACK else "O")
        
        if current_player == WHITE:
            handle_ai_turn(board, current_player)
        else:
            handle_player_turn(board, current_player)
        
        current_player = -current_player
    
    display_game_result(board)

def handle_ai_turn(board, player):
    row, col = get_min_max_move(board, player)
    if row == -1 and col == -1:
        print("O HAS NO MOVEMENTS")
    else:
        make_move(board, player, (row, col))

def handle_player_turn(board, player):
    valid_moves = get_valid_moves(board, player)
    print("My Movements:", valid_moves)
    
    if not valid_moves:
        print("You have no movements available")
        return
    
    while True:
        try:
            row, col = get_player_input()
            if is_valid_move(valid_moves, (row, col)):
                make_move(board, player, (row, col))
                break
            print("Invalid move. Try again.")
        except ValueError:
            print("Invalid entry. Enter valid numbers.")

def get_player_input():
    row = int(input("ROW: "))
    col = int(input("COLUMN: "))
    return row, col

def display_game_result(board):
    print_board(board)
    black_score, white_score = get_score(board, BLACK, WHITE)
    print("States:", COUNTER)
    if black_score > white_score:
        print("X Won.")
    elif white_score > black_score:
        print("O Won.")
    else:
        print("Tie.")

if __name__ == "__main__":
    opcion = 0
    print(" PLAYER VS IA")
    start_time = time.time()
    play_othello_vs_ai()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")