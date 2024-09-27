import copy

COUNTER = 0
empty_cell = 0
BLACK = 1
WHITE = -1

def is_valid_move(valid_moves, move):
    if move in valid_moves:
        return True
    return False

def get_player_tokens(board, player, board_size):
    player_tokens = []
    for row in range(board_size):
        for column in range(board_size):
            if board[row][column] == player:
                player_tokens.append((row, column))
    return player_tokens

def get_score(board, black, white):
    black_score = sum(row.count(black) for row in board)
    white_score = sum(row.count(white) for row in board)
    return black_score, white_score

def terminal_test(board, empty_cell):
    return all(all(cell != empty_cell for cell in row) for row in board)

def update_max_values(evaluation, max_val, move, best_move):
    if evaluation > max_val:
        return evaluation, move
    return max_val, best_move

def update_min_values(evaluation, min_val, move, best_move):
    if evaluation < min_val:
        return evaluation, move
    return min_val, best_move

def min_max_alpha_beta(board, player, alpha, beta, maximizing_player, get_valid_moves, make_move):
    global COUNTER
    COUNTER += 1

    if terminal_test(board, empty_cell):
        return get_score(board, BLACK, WHITE)[1], 0
    
    valid_moves = get_valid_moves(board, player)

    if maximizing_player:
        return maximize(board, player, alpha, beta, valid_moves, get_valid_moves, make_move)
    else:
        return minimize(board, player, alpha, beta, valid_moves, get_valid_moves, make_move)

def maximize(board, player, alpha, beta, valid_moves, get_valid_moves, make_move):
    max_val = float('-inf')
    best_move = None
    
    for move in valid_moves:
        new_board = simulate_move(board, player, move, make_move)
        evaluation, _ = min_max_alpha_beta(new_board, player, alpha, beta, False, get_valid_moves, make_move)

        if evaluation > max_val:
            max_val = evaluation
            best_move = move

        alpha = max(alpha, evaluation)
        if beta <= alpha:
            break
            
    return max_val, best_move

def minimize(board, player, alpha, beta, valid_moves, get_valid_moves, make_move):
    min_val = float('inf')
    best_move = None
    
    for move in valid_moves:
        new_board = simulate_move(board, -player, move, make_move)
        evaluation, _ = min_max_alpha_beta(new_board, player, alpha, beta, True, get_valid_moves, make_move)

        if evaluation < min_val:
            min_val = evaluation
            best_move = move

        beta = min(beta, evaluation)
        if beta <= alpha:
            break
            
    return min_val, best_move

def simulate_move(board, player, move, make_move):
    new_board = copy.deepcopy(board)
    make_move(new_board, player, move)
    return new_board
def get_min_max_move(board, player, get_valid_moves, make_move):
    valid_moves = get_valid_moves(board, player)
    if len(valid_moves) > 0:
        _, best_move = min_max_alpha_beta(board, player, float('-inf'), float('inf'), False, get_valid_moves, make_move)
        print("IA move: ", best_move)
        return best_move if best_move is not None else valid_moves[0]
    else:
        return (-1, -1)

def play_othello_vs_ai(initialize_board, print_board, get_valid_moves, make_move):
    board = initialize_board()
    current_player = BLACK
    while not terminal_test(board, empty_cell):
        print_board(board)
        print("Actual player:", "X" if current_player == BLACK else "O")
        
        if current_player == WHITE:
            handle_ai_turn(board, current_player, get_valid_moves, make_move)
        else:
            handle_player_turn(board, current_player, get_valid_moves, make_move)
        
        current_player = -current_player
    
    display_game_result(board)

def handle_ai_turn(board, player, get_valid_moves, make_move):
    row, col = get_min_max_move(board, player, get_valid_moves, make_move)
    if row == -1 and col == -1:
        print("O HAS NO MOVEMENTS")
    else:
        make_move(board, player, (row, col))

def handle_player_turn(board, player, get_valid_moves, make_move):
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
    score_black, score_white = get_score(board, BLACK, WHITE)
    print("Game Over")
    print(f"Score - Black (X): {score_black}, White (O): {score_white}")
    if score_black > score_white:
        print("Black (X) wins!")
    elif score_white > score_black:
        print("White (O) wins!")
    else:
        print("It's a tie!")